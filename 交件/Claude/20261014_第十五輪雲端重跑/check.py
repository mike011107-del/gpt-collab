#!/usr/bin/env python3
"""第十五輪八組配色：可在雲端重跑的檢查程式。

只用 Python 標準函式庫，不依賴 Claude 暫存區或 cl.py。
用法（在本資料夾）：python3 check.py
輸出：結果/結果.json、結果/對比逐對.csv、結果/差異表.md
退出碼：0＝自我測試通過且八組都算完；1＝自我測試失敗；2＝輸入有缺。

三類結果分開放：
- public：公開公式，任何人可用其他工具重算（WCAG 對比、CIEDE2000、Machado 色弱模擬、APCA、RAL 最近色號）。
- custom_model：Claude 自訂的評分模型（同行 15、誤認 20、遠看 15、色弱 10）。規則照原程式重寫，權重是自訂的，不是業界標準，也不是已證實的市場效果。
- private：命格 30 與「只屬崧淳」10。依據不公開或屬主觀判斷，這裡只轉錄原報告值，標「未獨立驗證」，不重算、不加總。
"""
import json, math, os, sys, csv, platform

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, '輸入')
OUT = os.path.join(HERE, '結果')

# ---------- 色彩數學（標準版） ----------
def rgb(h):
    h = h.lstrip('#'); return [int(h[i:i+2], 16) for i in (0, 2, 4)]
def hx(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)
def dec(v):  # sRGB 解碼（IEC 61966-2-1；WCAG 2.2 也改用 0.04045）
    v /= 255; return v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4
def enc(v):
    v = max(0.0, min(1.0, v)); return 255*(12.92*v if v <= 0.0031308 else 1.055*v**(1/2.4)-0.055)
def lin3(h): return [dec(v) for v in rgb(h)]
def from_lin(c): return hx([enc(v) for v in c])
def lum(h):
    r, g, b = lin3(h); return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(a, b):  # WCAG 2.x contrast ratio
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x+0.05)/(y+0.05)

# sRGB → XYZ（D65），IEC 61966-2-1 矩陣；白點取矩陣列和，使白色恰為 L*=100, a*=b*=0
M = [[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]
WHITE = [sum(r) for r in M]
EPS, KAP = 216/24389, 24389/27
def lab_std(h):
    c = lin3(h); X, Yv, Z = [sum(M[i][j]*c[j] for j in range(3))/WHITE[i] for i in range(3)]
    f = lambda t: t**(1/3) if t > EPS else (KAP*t+16)/116
    return (116*f(Yv)-16, 500*(f(X)-f(Yv)), 200*(f(Yv)-f(Z)))
# 相容模式：照原程式 cl.lab 的四位小數矩陣與舊門檻，用來確認原數字能否重現
def lab_compat(h):
    def lin(c):
        c /= 255; return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    r, g, b = [lin(x) for x in rgb(h)]
    X = (0.4124*r+0.3576*g+0.1805*b)/0.95047; Yv = 0.2126*r+0.7152*g+0.0722*b; Z = (0.0193*r+0.1192*g+0.9505*b)/1.08883
    f = lambda t: t**(1/3) if t > 0.008856 else 7.787*t+16/116
    return (116*f(Yv)-16, 500*(f(X)-f(Yv)), 200*(f(Yv)-f(Z)))

def de2000_lab(l1, l2):  # Sharma, Wu, Dalal (2005) 的寫法
    L1, a1, b1 = l1; L2, a2, b2 = l2
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2); Cb = (C1+C2)/2
    G = 0.5*(1-math.sqrt(Cb**7/(Cb**7+25**7)))
    a1p, a2p = (1+G)*a1, (1+G)*a2; C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dL = L2-L1; dC = C2p-C1p
    if C1p*C2p == 0: dh = 0
    else:
        dh = h2p-h1p
        if dh > 180: dh -= 360
        elif dh < -180: dh += 360
    dH = 2*math.sqrt(C1p*C2p)*math.sin(math.radians(dh/2))
    Lb = (L1+L2)/2; Cbp = (C1p+C2p)/2
    if C1p*C2p == 0: hb = h1p+h2p
    elif abs(h1p-h2p) <= 180: hb = (h1p+h2p)/2
    elif h1p+h2p < 360: hb = (h1p+h2p+360)/2
    else: hb = (h1p+h2p-360)/2
    T = 1-0.17*math.cos(math.radians(hb-30))+0.24*math.cos(math.radians(2*hb))+0.32*math.cos(math.radians(3*hb+6))-0.20*math.cos(math.radians(4*hb-63))
    dth = 30*math.exp(-((hb-275)/25)**2); RC = 2*math.sqrt(Cbp**7/(Cbp**7+25**7))
    SL = 1+0.015*(Lb-50)**2/math.sqrt(20+(Lb-50)**2); SC = 1+0.045*Cbp; SH = 1+0.015*Cbp*T; RT = -math.sin(math.radians(2*dth))*RC
    return math.sqrt((dL/SL)**2+(dC/SC)**2+(dH/SH)**2+RT*(dC/SC)*(dH/SH))

MODE = {'std': lab_std, 'compat': lab_compat}
def de(h1, h2, mode='std'):
    f = MODE[mode]; return de2000_lab(f(h1), f(h2))
def lch(h, mode='std'):
    L, a, b = MODE[mode](h); return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

# Machado, Oliveira, Fernandes (2009) severity 1.0，作用在線性 RGB
MACH = {'protan': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
        'deutan': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
        'tritan': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}
def cvd(h, kind):
    c = lin3(h); m = MACH[kind]; return from_lin([sum(m[i][j]*c[j] for j in range(3)) for i in range(3)])

# APCA 0.1.9（apca-w3 的常數），回傳 Lc
def apca(text, bg):
    def Y(h):
        r, g, b = [v/255 for v in rgb(h)]; return 0.2126729*r**2.4+0.7151522*g**2.4+0.0721750*b**2.4
    t, b = Y(text), Y(bg)
    t = t if t > 0.022 else t+(0.022-t)**1.414; b = b if b > 0.022 else b+(0.022-b)**1.414
    if abs(b-t) < 0.0005: return 0.0
    if b > t:
        s = (b**0.56-t**0.57)*1.14; out = 0 if s < 0.1 else s-0.027
    else:
        s = (b**0.65-t**0.62)*1.14; out = 0 if s > -0.1 else s+0.027
    return out*100

# 霧中（自訂模型）：線性 RGB 中與霧色 #C9CCCC 以 55% 混合
def fog(h, k=0.55, fogc='#C9CCCC'):
    a = lin3(h); b = lin3(fogc); return from_lin([a[i]*(1-k)+b[i]*k for i in range(3)])

# ---------- 自我測試 ----------
SHARMA = [  # Sharma 2005 CIEDE2000 測試資料（L1,a1,b1,L2,a2,b2,ΔE00）節錄
    (50.0000, 2.6772, -79.7751, 50.0000, 0.0000, -82.7485, 2.0425),
    (50.0000, 0.0000, 0.0000, 50.0000, -1.0000, 2.0000, 2.3669),
    (50.0000, 2.5000, 0.0000, 73.0000, 25.0000, -18.0000, 27.1492),
    (60.2574, -34.0099, 36.2677, 60.4626, -34.1751, 39.4387, 1.2644),
    (2.0776, 0.0795, -1.1350, 0.9033, -0.0636, -0.5514, 0.9082),
]
def selftest():
    errs = []
    for t in SHARMA:
        got = de2000_lab(t[0:3], t[3:6])
        if abs(got-t[6]) > 1e-4: errs.append(f'CIEDE2000 {t} 得 {got:.4f}')
    if abs(contrast('#000000', '#FFFFFF')-21) > 1e-9: errs.append('WCAG 黑白對比不是 21')
    L, a, b = lab_std('#FFFFFF')
    if abs(L-100) > 1e-6 or abs(a) > 1e-6 or abs(b) > 1e-6: errs.append('白色 Lab 不是 (100,0,0)')
    for k in MACH:  # Machado 矩陣每列和應約為 1（白色不變）
        for row in MACH[k]:
            if abs(sum(row)-1) > 1e-3: errs.append(f'{k} 矩陣列和 {sum(row)}')
    return errs

# ---------- 評分（自訂模型，照原程式 sets.py market() 重寫） ----------
def clamp(x): return max(0.0, min(1.0, x))
def text_on(h, dk, wh): return dk if contrast(dk, h) >= contrast(wh, h) else wh

def evaluate(g, Y, peers, mode, dk, wh):
    m = g['colors'][0]['hex']; t = g['colors'][2]['hex']; share = [c['share'] for c in g['colors']]
    o = {}
    # 同行 15
    near = min((de(m, p['hex'], mode), p['company'], p['hex']) for p in peers)
    n15 = sum(1 for p in peers if de(m, p['hex'], mode) < 15)
    o['同行'] = round(15*(0.5*clamp((near[0]-3)/12)+0.5*clamp(1-n15/6)), 1); o['同行近色家數'] = n15
    o['同行最近'] = {'ΔE2000': round(near[0], 2), 'company': near[1], 'hex': near[2]}
    # 誤認 20
    pen = []; Lm, Cm, Hm = lch(m, mode)
    d_cht = de(m, '#0069AA', mode)
    if d_cht < 15: pen.append(['像中華電信黃車配藍', 8])
    elif d_cht < 25 and 230 <= Hm <= 290: pen.append(['偏中華電信藍', 4])
    if min(de(m, '#005E83', mode), de(m, '#1E5B8A', mode)) < 12: pen.append(['像業主告示牌藍', 6])
    if min(de(m, '#308446', mode), de(m, '#2E8B57', mode)) < 12: pen.append(['像圍籬綠或台南垃圾車', 5])
    if Lm > 85: pen.append(['大面積淺色，遠看可能像白色回收車', 4])
    if share[1] >= 50: pen.append(['車身以黃為主', 7])
    if min(de(t, '#DA530A', mode), de(t, '#F82F22', mode)) < 12: pen.append(['第三色靠近交維橙', 3])
    o['誤認'] = round(max(0, 20-sum(p[1] for p in pen)), 1); o['誤認扣分'] = pen
    # 遠看 15
    tx = text_on(m, dk, wh)
    pairs = [(m, Y), (m, t), (Y, t), (m, tx)]
    best = max(pairs, key=lambda p: contrast(*p)); r = contrast(*best); rf = contrast(fog(best[0]), fog(best[1])); rmy = contrast(m, Y)
    o['遠看'] = round(15*(0.4*clamp((rmy-1.2)/3.8)+0.4*clamp((r-1.5)/6)+0.2*clamp((rf-1.1)/1.9)), 1)
    o['對比'] = {'主黃': round(rmy, 2), '最強一對': round(r, 2), '霧中': round(rf, 2), '最強一對色碼': list(best)}
    # 色弱 10（原程式只看紅、綠色弱）
    mins = []
    for kind in ('protan', 'deutan'):
        a, b, c = cvd(m, kind), cvd(Y, kind), cvd(t, kind)
        mins.append(min(de(a, b, mode), de(a, c, mode), de(b, c, mode)))
    o['色弱'] = round(10*clamp((min(mins)-5)/20), 1); o['色弱最小ΔE'] = round(min(mins), 1)
    return o

def public(g, Y, peersA, peersB, site, ral, dk, wh):
    cs = g['colors']; m = cs[0]['hex']
    names = {c['hex']: f"{c['role']}{c['name']}" for c in cs}
    pairs = []
    for i in range(3):
        for j in range(i+1, 3):
            a, b = cs[i], cs[j]
            pairs.append({'A': f"{a['role']} {a['name']} {a['hex']}", 'B': f"{b['role']} {b['name']} {b['hex']}",
                          'WCAG對比': round(contrast(a['hex'], b['hex']), 2),
                          'APCA_Lc_A字在B上': round(apca(a['hex'], b['hex']), 1), 'APCA_Lc_B字在A上': round(apca(b['hex'], a['hex']), 1),
                          'ΔE2000': round(de(a['hex'], b['hex']), 2)})
    tx = text_on(m, dk, wh)
    text = {'主色上的字色': tx, 'WCAG對比': round(contrast(tx, m), 2), 'APCA_Lc': round(apca(tx, m), 1),
            '黃上的深字': {'hex': dk, 'WCAG對比': round(contrast(dk, Y), 2)}, '黃上的白字': {'hex': wh, 'WCAG對比': round(contrast(wh, Y), 2)}}
    cv = {}
    for kind in ('protan', 'deutan', 'tritan'):
        sim = [cvd(c['hex'], kind) for c in cs]
        ds = [(de(sim[i], sim[j]), cs[i]['role'], cs[j]['role']) for i in range(3) for j in range(i+1, 3)]
        mn = min(ds)
        cv[kind] = {'模擬後色碼': sim, '最小ΔE2000': round(mn[0], 2), '最接近的一對': f'{mn[1]}／{mn[2]}'}
    gray = {c['role']: round(lum(c['hex']), 4) for c in cs}
    def nearest(h, L, key='hex'):
        r = min((de(h, p[key]), p) for p in L); return {'ΔE2000': round(r[0], 2), **{k: v for k, v in r[1].items()}}
    def near_ral(h):
        by_rgb = min((de(h, hx(v['rgb'])), k, v['name']) for k, v in ral.items())
        L1 = lab_std(h)
        by_lab = min((de2000_lab(L1, tuple(v['lab'])), k, v['name']) for k, v in ral.items())
        return {'依RGB欄': {'RAL': by_rgb[1], 'name': by_rgb[2], 'ΔE2000': round(by_rgb[0], 2)},
                '依Lab欄': {'RAL': by_lab[1], 'name': by_lab[2], 'ΔE2000': round(by_lab[0], 2)}}
    return {'逐對': pairs, '字色': text, '色弱模擬': cv, '相對亮度': gray,
            '同行最近_A清單': {c['role']: nearest(c['hex'], peersA) for c in cs},
            '同行最近_B清單': {c['role']: nearest(c['hex'], peersB) for c in cs},
            '主色ΔE<15同行數_A': sum(1 for p in peersA if de(m, p['hex']) < 15),
            '主色ΔE<15同行數_B': sum(1 for p in peersB if de(m, p['hex']) < 15),
            '工地與公共車輛最近': {c['role']: nearest(c['hex'], site) for c in cs},
            'RAL最近': {c['role']: near_ral(c['hex']) for c in cs}}

def main():
    errs = selftest()
    if errs:
        print('自我測試失敗：'); [print(' ', e) for e in errs]; return 1
    print('自我測試通過：CIEDE2000（Sharma 5 組）、WCAG 黑白 21:1、白點、Machado 矩陣列和')
    try:
        P = json.load(open(os.path.join(IN, '八組.json'), encoding='utf-8'))
        A = json.load(open(os.path.join(IN, '同業色_A_原程式53色.json'), encoding='utf-8'))['colors']
        B = json.load(open(os.path.join(IN, '同業色_B_總表全量.json'), encoding='utf-8'))['colors']
        S = json.load(open(os.path.join(IN, '參照色_誤認規則.json'), encoding='utf-8'))['site_colors']
        R = json.load(open(os.path.join(IN, 'RAL_wikipedia.json'), encoding='utf-8'))
        O = json.load(open(os.path.join(IN, '原報告值_分數.json'), encoding='utf-8'))
    except (OSError, ValueError, KeyError) as e:
        print('輸入有缺：', e); return 2
    Y = P['工程黃']['hex']; dk = P['文字色']['深']; wh = P['文字色']['白']
    res = {'環境': {'python': platform.python_version(), 'platform': platform.platform()}, 'groups': {}}
    rows = []; diff = []
    FIELDS = ['同行', '同行近色家數', '誤認', '遠看', '主黃', '最強一對', '霧中', '色弱', '色弱最小ΔE']
    for g in P['groups']:
        k = g['group']; o = O[g['key']]
        pub = public(g, Y, A, B, S, R, dk, wh)
        cm = {mode: evaluate(g, Y, A, mode, dk, wh) for mode in ('std', 'compat')}
        cmB = evaluate(g, Y, B, 'std', dk, wh)
        res['groups'][k] = {'輸入': g, 'public': pub,
            'custom_model': {'標準Lab': cm['std'], '原程式相容Lab': cm['compat'], '標準Lab_同行用B清單': cmB,
                             '說明': '自訂模型，權重不是業界標準，不代表已證實的市場效果'},
            'private': {'命格/30': o['fate30'], '只屬崧淳/10': {'1': 10, '2': 9, '3': 5, '4': 4}[k[0]],
                        '原報告市場/70': o['market70'], '狀態': '原報告值，未獨立驗證；本程式不重算、不加總'}}
        for p in pub['逐對']:
            rows.append([k, p['A'], p['B'], p['WCAG對比'], p['APCA_Lc_A字在B上'], p['APCA_Lc_B字在A上'], p['ΔE2000']])
        od = o['detail']; orig = {'同行': od['同行'], '同行近色家數': od['同行近色家數'], '誤認': od['誤認'], '遠看': od['遠看'],
            '主黃': od['對比']['主黃'], '最強一對': od['對比']['最強一對'], '霧中': od['對比']['霧中'], '色弱': od['色弱'], '色弱最小ΔE': od['色弱最小ΔE']}
        def flat(x): return {'同行': x['同行'], '同行近色家數': x['同行近色家數'], '誤認': x['誤認'], '遠看': x['遠看'],
            '主黃': x['對比']['主黃'], '最強一對': x['對比']['最強一對'], '霧中': x['對比']['霧中'], '色弱': x['色弱'], '色弱最小ΔE': x['色弱最小ΔE']}
        for f in FIELDS:
            diff.append([k, f, orig[f], flat(cm['compat'])[f], flat(cm['std'])[f], flat(cmB)[f]])
        # 原分數重算加總（只為比對；private 兩項用原值）
        sub = {m: round(cm[m]['同行']+cm[m]['誤認']+cm[m]['遠看']+cm[m]['色弱'], 1) for m in cm}
        res['groups'][k]['custom_model']['四項小計(滿分60)'] = {'原報告': round(o['market70']-{'1': 10, '2': 9, '3': 5, '4': 4}[k[0]], 1), **sub}
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, '結果.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, '對比逐對.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(['組', '色A', '色B', 'WCAG對比', 'APCA Lc（A字在B上）', 'APCA Lc（B字在A上）', 'ΔE2000（標準Lab）']); w.writerows(rows)
    with open(os.path.join(OUT, '差異表.md'), 'w', encoding='utf-8') as f:
        f.write('# 與原分數逐項比較（自動產生）\n\n欄位：原報告值｜相容模式重算（照原程式 Lab 公式）｜標準模式重算（IEC sRGB 矩陣＋CIE 常數）｜標準模式＋同行 B 清單（總表全量 61 色）\n\n')
        f.write('| 組 | 項目 | 原報告 | 相容重算 | 標準重算 | 標準＋B清單 | 相容＝原？ |\n|---|---|---|---|---|---|---|\n')
        for d in diff:
            f.write(f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} | {'是' if d[2] == d[3] else '**否**'} |\n")
    n_same = sum(1 for d in diff if d[2] == d[3])
    print(f'八組完成。原報告值 vs 相容模式：{n_same}/{len(diff)} 項相同。')
    for k, v in res['groups'].items():
        print(k, '小計60', v['custom_model']['四項小計(滿分60)'])
    return 0

if __name__ == '__main__':
    sys.exit(main())
