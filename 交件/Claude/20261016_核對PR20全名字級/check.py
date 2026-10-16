"""核對 GPT PR #20「名稱先行全名字級實作」的量測 JSON。

只讀 GPT 交的 JSON，不改它。只用標準函式庫。
執行：python3 check.py   （從本資料夾執行；輸出 結果.json）
退出碼 0＝所有「單項變更」檢查通過；1＝有不一致。
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "GPT" / "20261016_名稱先行全名字級實作.json"
PREV = HERE.parent.parent / "GPT" / "20261016_名稱先行字距實作.json"
FULL_NAME = "崧淳環保科技股份有限公司"
TOL = 0.01  # CSS px


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def px(s):
    return float(str(s).replace("px", ""))


def main():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    prev = json.loads(PREV.read_text(encoding="utf-8"))
    ms = d["measurements"]
    fp = d["final_presentation_measurements"]
    out = {"來源": {"檔案": str(SRC.relative_to(HERE.parent.parent.parent)), "sha256": sha256(SRC)}}
    bad = []

    # 1. 固定區塊在 6＋2 張量測裡是否完全相同
    ref = ms[0]["fixed"]
    diffs = []
    for m in ms + fp:
        if m["fixed"] != ref:
            diffs.append(f'{m["variant"]}@{m["scale"]}')
    out["固定區塊完全相同"] = not diffs
    if diffs:
        bad.append(("固定區塊不同", diffs))

    # 2. 全名除字級外的屬性是否相同
    keys = ["letter_spacing", "line_height", "font_weight", "font", "color", "background", "paper", "full_text_lines"]
    other = {k: sorted({json.dumps(m[k], sort_keys=True) for m in ms + fp}) for k in keys}
    out["全名其他屬性"] = {k: (json.loads(v[0]) if len(v) == 1 else [json.loads(x) for x in v]) for k, v in other.items()}
    varied = [k for k, v in other.items() if len(v) > 1]
    # 全名行框是浮點數，用容差比
    fb0 = ms[0]["full_box"]
    fb_diff = max(abs(m["full_box"][k] - fb0[k]) for m in ms + fp for k in fb0)
    out["全名行框最大差px"] = fb_diff
    if fb_diff > TOL:
        varied.append("full_box")
    out["全名其他屬性有變動的欄位"] = varied
    if varied:
        bad.append(("全名其他屬性有變動", varied))

    # 3. 全名框寬＝字數×字級＋字數×字距（瀏覽器字框含最後一字後的字距）
    ls = px(ms[0]["letter_spacing"])
    n = len(FULL_NAME)
    rows = []
    for m in ms:
        s = m["size_px"]
        tb = m["full_text_box_not_ink_bounds"]
        expect = n * s + n * ls
        rows.append({"版本": m["variant"], "倍率": m["scale"], "字級px": s, "量得框寬": round(tb["width"], 4), "算式框寬": round(expect, 4), "差": round(tb["width"] - expect, 4)})
        if abs(tb["width"] - expect) > TOL:
            bad.append(("框寬不符算式", m["variant"]))
    out["框寬算式"] = {"算式": f"{n}字×字級＋{n}×{ls}px", "逐張": rows}

    # 4. 全名字框上下緣與上下鄰近區塊的距離（都是瀏覽器框，不是墨色）
    fixed = {f["class"]: f["box"] for f in ref}
    name_bottom = fixed["sc-name"]["top"] + fixed["sc-name"]["height"]
    svc_top = fixed["sc-services"]["top"]
    fb = ms[0]["full_box"]
    gaps = []
    for m in [x for x in ms if x["scale"] == 1]:
        tb = m["full_text_box_not_ink_bounds"]
        top, bottom = tb["top"], tb["top"] + tb["height"]
        gaps.append({
            "版本": m["variant"], "字級px": m["size_px"],
            "字框上緣": round(top, 2), "字框下緣": round(bottom, 2),
            "超出固定行框上方": round(max(0, fb["top"] - top), 2),
            "超出固定行框下方": round(max(0, bottom - (fb["top"] + fb["height"])), 2),
            "距主名框底": round(top - name_bottom, 2),
            "距工項框頂": round(svc_top - bottom, 2),
        })
    out["全名字框與鄰近區塊"] = {"主名框底": round(name_bottom, 2), "工項框頂": svc_top, "固定行框": [round(fb["top"], 2), round(fb["top"] + fb["height"], 2)], "逐稿": gaps}
    if any(g["距主名框底"] <= 0 or g["距工項框頂"] <= 0 for g in gaps):
        bad.append(("全名字框碰到鄰近區塊", gaps))

    # 5. 字級比例：跟基準（原稿 17px）比
    main_px = px([f for f in ref if f["class"] == "sc-name"][0]["size"])
    svc_px = px([f for f in ref if f["class"] == "sc-services"][0]["size"])
    base = 17
    ratio = []
    for s in (17, 20, 24):
        ratio.append({
            "全名字級px": s,
            "相對原稿": round(s / base, 3),
            "50%預覽實際px": s * 0.5,
            "工項50%實際px": svc_px * 0.5,
            "全名÷工項": round(s / svc_px, 3),
            "主名÷全名": round(main_px / s, 3),
            "全名字重": int(ms[0]["font_weight"]),
            "工項字重": int([f for f in ref if f["class"] == "sc-services"][0]["weight"]),
        })
    out["字級比例"] = {"主名px": main_px, "工項px": svc_px, "逐稿": ratio}

    # 6. 換算到車身（推論）：道安規則第 42 條第三項，車廂兩邊所有人名稱
    #    大型車每字至少 25 cm 見方、小型車 16 cm；條文出處見
    #    交件/Claude/20261014_第十五輪雲端重跑/來源清冊.md 第 4 節。
    #    假設：全名照試排比例放大、「見方」約等於字級（em 框），只是比例換算。
    conv = []
    for cm in (25, 16):
        for s in (17, 20, 24):
            k = cm / s
            conv.append({
                "全名每字cm": cm, "試排全名px": s,
                "主名每字cm": round(main_px * k, 1),
                "全名總長cm": round((n * s + n * ls) * k, 1),
                "工項每字cm": round(svc_px * k, 1),
            })
    out["車身比例換算_推論"] = conv

    # 7. JSON 內部一致性：方法來源段落的描述是否仍是上一輪（字距）
    msrc = d.get("method_sources_reused_not_freshly_browsed", {})
    stale = {k: msrc.get(k) for k in ("scope", "variable") if "間距" in str(msrc.get(k, ""))}
    out["方法來源段落沿用上一輪描述"] = stale
    out["本輪scope欄"] = d.get("scope")

    # 8. 基準能不能從專案庫內的檔案核對
    out["基準可核對範圍"] = {
        "上一輪JSON有原稿HTML雜湊": "source_sha256" in prev,
        "本輪JSON有原稿HTML雜湊": "source_sha256" in d,
        "上一輪JSON有全名幾何": "full_box" in json.dumps(prev),
        "上一輪主名字級px": prev["fixed_conditions"]["name_size_px"],
        "本輪主名字級px": main_px,
        "上一輪原稿字距": [v["computed_tracking"] for v in prev["variants"] if v["name"] == "原稿"][0],
        "本輪主名字距": [f for f in ref if f["class"] == "sc-name"][0]["letter_spacing"],
        "上一輪墨色": prev["fixed_conditions"]["ink"],
        "本輪墨色": ms[0]["color"],
        "上一輪畫布": prev["fixed_conditions"]["canvas_css_px"],
        "本輪畫布": [ms[0]["paper"]["width"], ms[0]["paper"]["height"]],
    }

    out["不一致"] = [str(b) for b in bad]
    (HERE / "結果.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("不一致：", len(bad))
    for b in bad:
        print("  ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
