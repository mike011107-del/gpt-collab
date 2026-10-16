#!/usr/bin/env python3
"""把精準色號貼到 AutoIP 生的「空白白色表面」上，保留原圖光影與紙紋。

為什麼不用 AutoIP 直接畫顏色：實驗一（學習_20261016）指定 #009999 會被畫成藍色，
各色平均偏差 ΔE_ok 0.06–0.20，不能拿來判斷精確色。所以 AI 只負責場景，顏色由程式上。

做法：從種子點做洪水填充選出白色表面 → 以該面最亮處為白點，算每個像素的明暗比例 →
在線性 RGB 裡用目標色乘上明暗比例。白紙在陰影處多暗，色塊就一樣多暗。

用法：python3 recolour.py 規格.json
規格：{"src": "底圖.png", "out": "輸出.png",
       "surfaces": [{"seed": [x, y]（或 "poly": [[x,y],...]）, "tol": 28, "color": "#2071B5",
                     "stripe": {"color": "#D58401", "from": 0.86, "to": 0.94}}]}
stripe 是在該面高度的 from–to 比例處畫一條帶，逐欄計算，會跟著透視傾斜。
"""

import json
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw


def to_lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255


def hex_lin(h):
    h = h.lstrip("#")
    return to_lin(np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float))


def flood(img, seed, tol):
    """以顏色距離與局部連續做洪水填充，選出白色表面。"""
    H, W, _ = img.shape
    x0, y0 = seed
    ref = img[y0, x0].astype(float)
    mask = np.zeros((H, W), bool)
    q = deque([(y0, x0)])
    mask[y0, x0] = True
    while q:
        y, x = q.popleft()
        here = img[y, x].astype(float)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and not mask[ny, nx]:
                p = img[ny, nx].astype(float)
                # 同時限制「離種子色」與「離鄰點」，避免漏到白牆
                if np.abs(p - here).max() < 6 and np.abs(p - ref).max() < tol:
                    mask[ny, nx] = True
                    q.append((ny, nx))
    return mask


def poly_mask(shape, pts):
    m = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
    return np.array(m) > 0


def soften(mask):
    """邊緣羽化 1px，避免鋸齒。"""
    m = mask.astype(float)
    pad = np.pad(m, 1, mode="edge")
    blur = sum(pad[1 + dy:1 + dy + m.shape[0], 1 + dx:1 + dx + m.shape[1]]
               for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9
    return np.where(mask, np.maximum(blur, 0.5), blur * 0.6)


def apply(img, mask, color_lin):
    lin = to_lin(img.astype(float))
    lum = lin @ np.array([0.2126, 0.7152, 0.0722])
    white = np.percentile(lum[mask], 97)
    shade = np.clip(lum / max(white, 1e-6), 0, 1.05)[..., None]
    painted = color_lin[None, None, :] * shade
    a = soften(mask)[..., None]
    return to_srgb(lin * (1 - a) + painted * a)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    img = np.array(Image.open(spec["src"]).convert("RGB"))
    out = img.astype(float)
    for s in spec["surfaces"]:
        # 有反光漸層的面洪水填充會漏選，改給四角座標 poly
        m = poly_mask(img.shape, s["poly"]) if "poly" in s else flood(img, s["seed"], s.get("tol", 28))
        if s.get("color"):
            out = apply(out.astype(np.uint8), m, hex_lin(s["color"]))
        st = s.get("stripe")
        if st:
            # 逐欄算該面的上下緣，色帶跟著面的透視斜度走
            # 上下緣用直線擬合（取各欄中段 80% 的穩健值），避免邊緣雜點造成鋸齒
            band = np.zeros_like(m)
            xs = np.where(m.sum(0) > 3)[0]
            tops = np.array([np.where(m[:, x])[0].min() for x in xs])
            bots = np.array([np.where(m[:, x])[0].max() for x in xs])
            fit = []
            for v in (tops, bots):
                keep = np.abs(v - np.median(v - np.polyval(np.polyfit(xs, v, 1), xs))
                              - np.polyval(np.polyfit(xs, v, 1), xs)) < 4
                fit.append(np.polyfit(xs[keep], v[keep], 1))
            for x in xs:
                top, bot = np.polyval(fit[0], x), np.polyval(fit[1], x)
                y1 = int(round(top + (bot - top) * st["from"]))
                y2 = int(round(top + (bot - top) * st["to"]))
                band[y1:y2, x] = m[y1:y2, x]
            # 色帶的明暗取原底圖，不取已上色的結果
            painted = apply(img, band, hex_lin(st["color"]))
            out = np.where(band[..., None], painted, out)
    Image.fromarray(out.round().astype(np.uint8)).save(spec["out"], quality=92)
    print(spec["out"])


if __name__ == "__main__":
    main()
