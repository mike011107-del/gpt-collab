"""LOGO 設計教學課程的示意圖（全部自繪，無第三方圖）。
每個函式回傳一段 SVG 字串。練習用形狀不是崧淳 LOGO 提案。"""
import math

B, Y, R, G = '#194764', '#F39D16', '#D73626', '#E2E9EF'
INK, MID, LIGHT = '#1b1b1b', '#8a8a8a', '#d9d9d9'
FONT = "font-family=\"'Noto Sans TC', sans-serif\""


def svg(w, h, body, cls='fig'):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def t(x, y, s, size=9, anchor='middle', fill=INK, weight=400):
    return f'<text x="{x}" y="{y}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{s}</text>'


# ---------- 練習用形狀：圓＋橫條＋小方塊 ----------
def mark(x, y, s, c1=INK, c2=INK, c3=INK, gap=0.10, bg='#fff'):
    """s＝寬。圓分上下兩半，中間白縫，右側小方塊。"""
    r = s * 0.42
    cx, cy = x + s * 0.45, y + s / 2
    g = s * gap
    top = f'<path d="M{cx-r},{cy-g/2} A{r},{r} 0 0 1 {cx+r},{cy-g/2} Z" fill="{c1}"/>'
    bot = f'<path d="M{cx-r},{cy+g/2} A{r},{r} 0 0 0 {cx+r},{cy+g/2} Z" fill="{c2}"/>'
    sq = s * 0.14
    box = f'<rect x="{cx+r+s*0.03}" y="{cy-sq/2}" width="{sq}" height="{sq}" fill="{c3}"/>'
    return top + bot + box


# ---------- 第 1 課：LOGO 與識別系統 ----------
def f_system():
    items = ['名片', '車身', '制服', '報價單', '網站', '招牌']
    b = ''
    cx, cy = 210, 95
    b += f'<rect x="{cx-38}" y="{cy-24}" width="76" height="48" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    b += t(cx, cy + 4, 'LOGO', 12, weight=700)
    for i, s in enumerate(items):
        a = math.radians(-90 + i * 60)
        x, y = cx + math.cos(a) * 150, cy + math.sin(a) * 68
        b += f'<line x1="{cx+math.cos(a)*44}" y1="{cy+math.sin(a)*27}" x2="{x-math.cos(a)*30}" y2="{y-math.sin(a)*12}" stroke="{MID}" stroke-width="0.8"/>'
        b += f'<rect x="{x-30}" y="{y-12}" width="60" height="24" rx="2" fill="#f4f4f4" stroke="{LIGHT}"/>'
        b += t(x, y + 3.5, s, 9.5)
    b += t(210, 186, '識別系統＝LOGO＋每個物件上的規則（位置、大小、顏色、留白、字）', 9, fill='#444')
    return svg(420, 195, b)


# ---------- 第 2 課：七種類型（虛構名稱「示例」） ----------
def f_types():
    b = ''
    W = 120
    def cell(i, row, label, sub, inner):
        x = 10 + i * W
        y = 8 + row * 128
        return (f'<rect x="{x}" y="{y}" width="{W-12}" height="96" fill="#fafafa" stroke="{LIGHT}"/>' + inner(x, y)
                + t(x + (W - 12) / 2, y + 110, label, 9.5, weight=700) + t(x + (W - 12) / 2, y + 122, sub, 7.5, fill='#555'))
    def wordmark(x, y):
        return t(x + 54, y + 58, '示例工程', 19, weight=900)
    def letter(x, y):
        return t(x + 54, y + 64, 'SL', 34, weight=900)
    def pict(x, y):  # 房子
        return f'<path d="M{x+30},{y+52} L{x+54},{y+26} L{x+78},{y+52} L{x+72},{y+52} L{x+72},{y+76} L{x+36},{y+76} L{x+36},{y+52} Z" fill="{INK}"/><rect x="{x+49}" y="{y+60}" width="10" height="16" fill="#fafafa"/>'
    def abstract(x, y):
        return (f'<circle cx="{x+46}" cy="{y+48}" r="20" fill="{INK}"/><circle cx="{x+64}" cy="{y+48}" r="20" fill="none" stroke="{INK}" stroke-width="6"/>')
    def mascot(x, y):
        return (f'<circle cx="{x+54}" cy="{y+48}" r="27" fill="{INK}"/><circle cx="{x+45}" cy="{y+43}" r="4" fill="#fff"/><circle cx="{x+63}" cy="{y+43}" r="4" fill="#fff"/>'
                f'<path d="M{x+44},{y+56} Q{x+54},{y+65} {x+64},{y+56}" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>'
                f'<circle cx="{x+33}" cy="{y+25}" r="8" fill="{INK}"/><circle cx="{x+75}" cy="{y+25}" r="8" fill="{INK}"/>')
    def emblem(x, y):
        cx, cy = x + 54, y + 48
        s = f'<circle cx="{cx}" cy="{cy}" r="37" fill="none" stroke="{INK}" stroke-width="3.5"/><circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{INK}" stroke-width="1"/>'
        k = 0.8
        pts = [(0,-12),(4,-3),(13,-3),(6,3),(9,12),(0,6),(-9,12),(-6,3),(-13,-3),(-4,-3)]
        s += '<path d="M' + ' L'.join(f'{cx+px*k},{cy-8+py*k}' for px, py in pts) + f' Z" fill="{INK}"/>'
        s += t(cx, cy + 17, '示例工程', 8.5, weight=700)
        return s
    def combo(x, y):
        return (f'<circle cx="{x+20}" cy="{y+48}" r="12" fill="{INK}"/><circle cx="{x+31}" cy="{y+48}" r="12" fill="none" stroke="{INK}" stroke-width="4"/>'
                + t(x + 50, y + 52.5, '示例工程', 12, 'start', weight=900))
    b += cell(0, 0, '字標', 'wordmark：整個名字', wordmark)
    b += cell(1, 0, '字母標', 'lettermark：縮寫', letter)
    b += cell(2, 0, '具象圖形標', 'pictorial：看得出的物', pict)
    b += cell(0, 1, '抽象圖形標', 'abstract：不指具體物', abstract)
    b += cell(1, 1, '吉祥物', 'mascot：角色', mascot)
    b += cell(2, 1, '徽章', 'emblem：字在框或徽裡', emblem)
    b += cell(3, 0, '組合標', 'combination：圖形＋名字', combo)
    b += t(424, 190, '「示例工程」是虛構名稱，', 8, 'middle', '#555') + t(424, 202, '圖是白澤自繪的類型示意，', 8, 'middle', '#555') + t(424, 214, '不是任何公司的標誌。', 8, 'middle', '#555')
    return svg(490, 262, b)


# ---------- 第 4 課：格式塔五條 ----------
def f_gestalt():
    b = ''
    W = 98
    labels = [('封閉', '缺口會被補成完整形'), ('圖地', '空白也被看成形'), ('相似', '長得像的歸成一組'), ('接近', '靠近的歸成一組'), ('連續', '眼睛沿順的線走')]
    for i, (a, c) in enumerate(labels):
        x = 6 + i * W
        b += f'<rect x="{x}" y="6" width="{W-8}" height="90" fill="#fafafa" stroke="{LIGHT}"/>'
        b += t(x + (W - 8) / 2, 110, a, 9.5, weight=700) + t(x + (W - 8) / 2, 122, c, 7.3, fill='#555')
    # 封閉：四段弧
    cx, cy, r = 6 + 45, 51, 28
    for k in range(4):
        a1, a2 = math.radians(k * 90 + 14), math.radians(k * 90 + 76)
        b += f'<path d="M{cx+r*math.cos(a1)},{cy+r*math.sin(a1)} A{r},{r} 0 0 1 {cx+r*math.cos(a2)},{cy+r*math.sin(a2)}" stroke="{INK}" stroke-width="7" fill="none"/>'
    # 圖地：四方塊與白十字
    x0 = 6 + W + 15
    for dx in (0, 1):
        for dy in (0, 1):
            b += f'<rect x="{x0+dx*33}" y="{18+dy*33}" width="27" height="27" fill="{INK}"/>'
    # 相似
    x0 = 6 + 2 * W + 15
    for col in range(4):
        for row in range(4):
            px, py = x0 + col * 18, 22 + row * 18
            if col == 1 or col == 3:
                b += f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="{INK}"/>'
            else:
                b += f'<circle cx="{px}" cy="{py}" r="5" fill="{INK}"/>'
    # 接近
    x0 = 6 + 3 * W + 10
    for grp in range(3):
        for row in range(4):
            for col in range(2):
                b += f'<circle cx="{x0+grp*26+col*10}" cy="{22+row*18}" r="4" fill="{INK}"/>'
    # 連續
    x0 = 6 + 4 * W
    b += f'<path d="M{x0+10},{80} C{x0+35},{80} {x0+55},{20} {x0+80},{20}" stroke="{INK}" stroke-width="5" fill="none"/>'
    b += f'<path d="M{x0+10},{20} C{x0+35},{20} {x0+55},{80} {x0+80},{80}" stroke="{MID}" stroke-width="5" fill="none"/>'
    return svg(496, 128, b)


# ---------- 第 4 課：細節 → 剪影 ----------
def f_silhouette():
    b = ''
    # 細節多的樹
    def tree_detail(x, y, s):
        o = f'<rect x="{x+s*0.46}" y="{y+s*0.55}" width="{s*0.08}" height="{s*0.4}" fill="{INK}"/>'
        import random
        rnd = random.Random(3)
        for _ in range(34):
            a = rnd.random() * 2 * math.pi
            d = rnd.random() * s * 0.28
            o += f'<circle cx="{x+s*0.5+math.cos(a)*d}" cy="{y+s*0.36+math.sin(a)*d*0.8}" r="{s*0.035+rnd.random()*s*0.03}" fill="none" stroke="{INK}" stroke-width="{s*0.012}"/>'
        for k in range(5):
            o += f'<line x1="{x+s*0.5}" y1="{y+s*0.6}" x2="{x+s*(0.3+k*0.1)}" y2="{y+s*0.42}" stroke="{INK}" stroke-width="{s*0.015}"/>'
        return o
    def tree_simple(x, y, s):
        return (f'<circle cx="{x+s*0.5}" cy="{y+s*0.38}" r="{s*0.3}" fill="{INK}"/>'
                f'<rect x="{x+s*0.44}" y="{y+s*0.55}" width="{s*0.12}" height="{s*0.4}" fill="{INK}"/>')
    b += tree_detail(10, 8, 110) + tree_simple(150, 8, 110)
    b += t(65, 132, '細節多：線、小圓、分枝', 8.5) + t(205, 132, '剪影：一個圓＋一根幹', 8.5)
    # 小尺寸
    b += t(300, 30, '縮到 12 px 大小', 8.5, 'start', '#555')
    b += f'<g transform="translate(300,40) scale(0.12)">{tree_detail(0,0,110)}</g>'
    b += f'<g transform="translate(330,40) scale(0.12)">{tree_simple(0,0,110)}</g>'
    b += t(300, 72, '左邊糊成灰點，右邊還是一棵樹', 8, 'start', '#555')
    return svg(440, 140, b)


# ---------- 第 5 課：負空間 ----------
def f_negative():
    b = ''
    def four(x, y, s, gap):
        q = (s - gap) / 2
        o = ''
        for dx in (0, 1):
            for dy in (0, 1):
                o += f'<rect x="{x+dx*(q+gap)}" y="{y+dy*(q+gap)}" width="{q}" height="{q}" fill="{INK}"/>'
        return o
    def arrow_cut(x, y, s):
        # 黑圓裡挖白箭頭
        cx, cy, r = x + s / 2, y + s / 2, s / 2
        a = (f'M{x+s*0.2},{y+s*0.43} L{x+s*0.55},{y+s*0.43} L{x+s*0.55},{y+s*0.28} L{x+s*0.82},{y+s*0.5} '
             f'L{x+s*0.55},{y+s*0.72} L{x+s*0.55},{y+s*0.57} L{x+s*0.2},{y+s*0.57} Z')
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}"/><path d="{a}" fill="#fff"/>'
    b += four(14, 10, 90, 4) + four(134, 10, 90, 14) + arrow_cut(254, 10, 90)
    b += t(59, 118, '縫 4%：大圖看得到十字', 8.5) + t(179, 118, '縫 16%：十字很清楚', 8.5) + t(299, 118, '黑圓裡的白箭頭', 8.5)
    # 縮小
    b += t(370, 22, '縮到 16 px', 8.5, 'start', '#555')
    b += f'<g transform="translate(370,32) scale(0.1778)">{four(0,0,90,4)}</g>'
    b += f'<g transform="translate(396,32) scale(0.1778)">{four(0,0,90,14)}</g>'
    b += f'<g transform="translate(422,32) scale(0.1778)">{arrow_cut(0,0,90)}</g>'
    b += t(370, 66, '細縫在螢幕上會被', 8, 'start', '#555') + t(370, 78, '模糊成灰線或消失', 8, 'start', '#555')
    b += t(370, 90, '（下一頁實際像素圖）', 8, 'start', '#555')
    return svg(470, 126, b)


# ---------- 第 6 課：視覺修正 ----------
def f_optical():
    b = ''
    def lines(x, y, w, top, base):
        return (f'<line x1="{x}" y1="{top}" x2="{x+w}" y2="{top}" stroke="{R}" stroke-width="0.6"/>'
                f'<line x1="{x}" y1="{base}" x2="{x+w}" y2="{base}" stroke="{R}" stroke-width="0.6"/>')
    # A 圓與方
    b += lines(8, 0, 104, 20, 80)
    b += f'<rect x="12" y="20" width="60" height="60" fill="{INK}"/><circle cx="98" cy="50" r="30" fill="{INK}" opacity="0"/>'
    b += f'<circle cx="104" cy="50" r="0" />'
    b = b.replace('<circle cx="98" cy="50" r="30" fill="#1b1b1b" opacity="0"/>', '')
    b += f'<rect x="10" y="20" width="44" height="60" fill="none"/>'
    # 改成兩組：方＋圓（同高）、方＋圓（圓加大 4%）
    b = ''
    b += lines(6, 0, 120, 24, 74)
    b += f'<rect x="10" y="24" width="50" height="50" fill="{INK}"/><circle cx="96" cy="49" r="25" fill="{INK}"/>'
    b += lines(140, 0, 120, 24, 74)
    b += f'<rect x="144" y="24" width="50" height="50" fill="{INK}"/><circle cx="230" cy="49" r="26.2" fill="{INK}"/>'
    b += t(66, 96, '同高：圓看起來比較小', 8.5) + t(200, 96, '圓上下各超出約 2.4%', 8.5)
    # B 十字
    def cross(x, y, s, hv, hh):
        return (f'<rect x="{x+s/2-hv/2}" y="{y}" width="{hv}" height="{s}" fill="{INK}"/>'
                f'<rect x="{x}" y="{y+s/2-hh/2}" width="{s}" height="{hh}" fill="{INK}"/>')
    b += cross(290, 22, 54, 12, 12) + cross(370, 22, 54, 12, 10.4)
    b += t(317, 96, '橫直同粗：橫的顯粗', 8.5) + t(397, 96, '橫改細 13%', 8.5)
    # C 三角
    b += lines(6, 0, 120, 120, 170)
    b += f'<rect x="10" y="120" width="50" height="50" fill="{INK}"/><path d="M70,170 L100,120 L130,170 Z" fill="{INK}"/>'
    b += lines(140, 0, 120, 120, 170)
    b += f'<rect x="144" y="120" width="50" height="50" fill="{INK}"/><path d="M204,171.5 L234,114 L264,171.5 Z" fill="{INK}"/>'
    b += t(66, 190, '尖端剛好碰線：三角顯矮', 8.5) + t(200, 190, '尖端超出線', 8.5)
    # D 視覺中心
    b += f'<rect x="290" y="112" width="60" height="64" fill="none" stroke="{MID}"/><rect x="310" y="134" width="20" height="20" fill="{INK}"/>'
    b += f'<rect x="370" y="112" width="60" height="64" fill="none" stroke="{MID}"/><rect x="390" y="131" width="20" height="20" fill="{INK}"/>'
    b += t(320, 190, '幾何正中：看起來偏低', 8.5) + t(400, 190, '略往上移', 8.5)
    b += t(220, 206, '紅線是基準線。修正量是示意，實際以眼睛判斷為準。', 8, fill='#555')
    return svg(440, 212, b)


# ---------- 第 6 課：用圓建構 ----------
def f_construct():
    b = ''
    cx1, cx2, cy, r = 70, 110, 70, 50
    for cx in (cx1, cx2):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{MID}" stroke-width="0.7" stroke-dasharray="3 2"/>'
    for x in range(10, 181, 20):
        b += f'<line x1="{x}" y1="10" x2="{x}" y2="130" stroke="{LIGHT}" stroke-width="0.5"/>'
    for y in range(10, 131, 20):
        b += f'<line x1="10" y1="{y}" x2="170" y2="{y}" stroke="{LIGHT}" stroke-width="0.5"/>'
    h = math.sqrt(r * r - 20 * 20)
    leaf = f'M90,{cy-h} A{r},{r} 0 0 1 90,{cy+h} A{r},{r} 0 0 1 90,{cy-h} Z'
    b += f'<path d="{leaf}" fill="{INK}" opacity="0.85"/>'
    b += f'<g transform="translate(230,0)"><path d="{leaf}" fill="{INK}"/></g>'
    b += t(90, 146, '建構：兩個同大的圓相交，取中間', 8.5) + t(320, 146, '成品：拿掉格線，只留形', 8.5)
    return svg(420, 152, b)


# ---------- 第 7 課：反白 ----------
def f_reverse():
    b = ''
    def ring(x, y, s, col, wgt):
        r = s * 0.36
        return (f'<circle cx="{x+s/2}" cy="{y+s/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{wgt}"/>'
                f'<rect x="{x+s*0.12}" y="{y+s/2-wgt/2}" width="{s*0.76}" height="{wgt}" fill="{col}"/>')
    b += f'<rect x="10" y="10" width="100" height="100" fill="#fff" stroke="{LIGHT}"/>' + ring(10, 10, 100, INK, 12)
    b += f'<rect x="130" y="10" width="100" height="100" fill="{INK}"/>' + ring(130, 10, 100, '#fff', 12)
    b += f'<rect x="250" y="10" width="100" height="100" fill="{INK}"/>' + ring(250, 10, 100, '#fff', 11.2)
    b += t(60, 128, '白底黑形（原稿）', 8.5) + t(180, 128, '反白，同樣粗細', 8.5) + t(300, 128, '反白，線改細約 7%', 8.5)
    b += t(180, 144, '螢幕上白形會顯粗；印刷時油墨會往白區吃，白形反而變細。要在實際媒材上比。', 8, fill='#555')
    return svg(360, 150, b)


# ---------- 第 9 課：四色、灰階與明度 ----------
COL4 = [(B, '主色 深藍灰', 28.5, 22.1, 203), (Y, '工程黃', 71.7, 76.6, 37), (R, '紅', 48.5, 77.1, 5), (G, '淺冷灰', 92.0, 3.9, 208)]


def grey_of(L):
    # L* → sRGB 灰
    fy = (L + 16) / 116
    Yv = fy ** 3 if fy > 6 / 29 else (L / 903.3)
    c = 12.92 * Yv if Yv <= 0.0031308 else 1.055 * Yv ** (1 / 2.4) - 0.055
    v = round(max(0, min(1, c)) * 255)
    return '#%02X%02X%02X' % (v, v, v)


def f_values():
    b = ''
    for i, (c, name, L, C, h) in enumerate(COL4):
        x = 30 + i * 100
        b += f'<rect x="{x}" y="10" width="90" height="46" fill="{c}" stroke="{LIGHT if c==G else c}"/>'
        b += f'<rect x="{x}" y="58" width="90" height="30" fill="{grey_of(L)}" stroke="{LIGHT}"/>'
        b += t(x + 45, 102, f'{name}', 8.5, weight=700) + t(x + 45, 114, c, 8)
        b += t(x + 45, 126, f'明度 L* {L}　彩度 C* {C}', 7.5, fill='#444')
    b += t(2, 36, '原色', 7.5, 'start', '#555') + t(2, 77, '灰階', 7.5, 'start', '#555')
    # 明度尺
    y0 = 150
    b += f'<line x1="20" y1="{y0}" x2="420" y2="{y0}" stroke="{INK}" stroke-width="0.8"/>'
    for v in range(0, 101, 10):
        x = 20 + v * 4
        b += f'<line x1="{x}" y1="{y0-3}" x2="{x}" y2="{y0+3}" stroke="{INK}" stroke-width="0.6"/>' + t(x, y0 + 13, str(v), 7)
    for c, name, L, C, h in COL4:
        x = 20 + L * 4
        b += f'<circle cx="{x}" cy="{y0-10}" r="6" fill="{c}" stroke="{INK}" stroke-width="0.5"/>'
    b += t(220, y0 + 27, '明度 L*：0 黑、100 白。四色落在 28、48、72、92，每兩色相差約 20，灰階下還分得開。', 8, fill='#444')
    return svg(430, 184, b)


def f_wheel():
    b = ''
    cx, cy, r1, r2 = 100, 100, 82, 58
    import colorsys
    for k in range(36):
        a1, a2 = math.radians(k * 10 - 90), math.radians(k * 10 + 10 - 90)
        rr, gg, bb = colorsys.hls_to_rgb(k * 10 / 360, 0.5, 0.75)
        col = '#%02X%02X%02X' % (int(rr * 255), int(gg * 255), int(bb * 255))
        p = (f'M{cx+r1*math.cos(a1)},{cy+r1*math.sin(a1)} A{r1},{r1} 0 0 1 {cx+r1*math.cos(a2)},{cy+r1*math.sin(a2)} '
             f'L{cx+r2*math.cos(a2)},{cy+r2*math.sin(a2)} A{r2},{r2} 0 0 0 {cx+r2*math.cos(a1)},{cy+r2*math.sin(a1)} Z')
        b += f'<path d="{p}" fill="{col}"/>'
    for c, name, L, C, h in COL4[:3]:
        a = math.radians(h - 90)
        x, y = cx + 44 * math.cos(a), cy + 44 * math.sin(a)
        b += f'<line x1="{cx}" y1="{cy}" x2="{cx+70*math.cos(a)}" y2="{cy+70*math.sin(a)}" stroke="{INK}" stroke-width="0.8"/>'
        b += f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
    b += t(cx, cy + r1 + 14, '色相環（HSL，飽和度與亮度固定）', 7.5, fill='#444')
    tx = 205
    lines = ['色相（HSL 角度，實測）', '深藍灰 #194764　約 203°', '工程黃 #F39D16　約 37°', '紅 #D73626　約 5°', '',
             '深藍灰與工程黃相差約 166°，', '接近色環兩端：互補色，對比強。', '紅與黃相差約 32°，是相鄰色。', '淺冷灰彩度只有 3.9，當中性色。']
    for i, s in enumerate(lines):
        b += t(tx, 40 + i * 15, s, 8.5, 'start', INK if i else INK, 700 if i == 0 else 400)
    return svg(420, 204, b)


# ---------- 第 10 課：幾色 ----------
def f_ncolours():
    b = ''
    sets = [('一色', B, B, B), ('二色', B, Y, B), ('三色', B, Y, R), ('四色全上', B, Y, R)]
    for i, (lab, c1, c2, c3) in enumerate(sets):
        x = 10 + i * 104
        bg = G if i == 3 else '#fff'
        b += f'<rect x="{x}" y="8" width="92" height="92" fill="{bg}" stroke="{LIGHT}"/>'
        b += mark(x + 8, 16, 76, c1, c2, c3)
        b += t(x + 46, 116, lab, 9, weight=700)
    b += t(57, 130, '最穩', 7.8, fill='#444') + t(161, 130, '主色＋黃', 7.8, fill='#444') + t(265, 130, '紅只佔小方塊', 7.8, fill='#444') + t(369, 130, '灰當底，不在標誌裡', 7.8, fill='#444')
    b += t(215, 148, '練習用形狀，不是崧淳 LOGO 提案。', 8, fill='#555')
    return svg(430, 154, b)


def f_proportion():
    b = ''
    segs = [(G, 56, '淺冷灰／白底'), (B, 30, '主色'), (Y, 10, '工程黃'), (R, 4, '紅')]
    x = 10
    for c, p, lab in segs:
        w = p * 4
        b += f'<rect x="{x}" y="10" width="{w}" height="30" fill="{c}" stroke="{LIGHT if c==G else c}"/>'
        x += w
    lx = 10
    for c, p, lab in segs:
        b += f'<rect x="{lx}" y="49" width="8" height="8" fill="{c}" stroke="{LIGHT if c==G else c}"/>' + t(lx + 12, 56.5, f'{lab} {p}%', 8, 'start')
        lx += 22 + len(lab) * 8 + 26
    b += t(210, 76, '一份文件或一面牆上的面積比例示意（白澤假設的數字，不是規範）。', 8, fill='#555')
    return svg(420, 82, b)


# ---------- 第 11 課：色弱模擬 ----------
SIM = {
    '一般': [B, Y, R, G],
    '第一型（紅弱）': ['#3A4765', '#BAA300', '#685D22', '#E7E9EF'],
    '第二型（綠弱）': ['#2F4063', '#CEB81C', '#90801D', '#E5E7EF'],
    '第三型（藍弱）': ['#004E51', '#FF8886', '#ED0034', '#DFEAEB'],
}


def f_cvd():
    b = ''
    for row, (lab, cols) in enumerate(SIM.items()):
        y = 8 + row * 34
        b += t(8, y + 19, lab, 8.5, 'start', weight=700 if row == 0 else 400)
        for i, c in enumerate(cols):
            b += f'<rect x="{100+i*62}" y="{y}" width="56" height="28" fill="{c}" stroke="{LIGHT}"/>'
        # 紅在深藍上
        b += f'<rect x="{360}" y="{y}" width="56" height="28" fill="{cols[0]}"/><rect x="{380}" y="{y+8}" width="16" height="12" fill="{cols[2]}"/>'
    for i, s in enumerate(['深藍灰', '工程黃', '紅', '淺冷灰']):
        b += t(128 + i * 62, 150, s, 8)
    b += t(388, 150, '紅放深藍上', 8)
    b += t(215, 166, 'Machado 2009 模型、嚴重度 1.0 的螢幕模擬（colour-tool 實算）。第一型下紅變成暗橄欖色，放在深藍上對比只剩 1.40。', 7.6, fill='#444')
    return svg(430, 172, b)


# ---------- 第 12 課：同色異底（Albers） ----------
def f_albers():
    b = ''
    bgs = [('#FFFFFF', '白底'), (B, '深藍底'), (R, '紅底'), ('#000000', '黑底')]
    for i, (bg, lab) in enumerate(bgs):
        x = 10 + i * 104
        b += f'<rect x="{x}" y="8" width="92" height="70" fill="{bg}" stroke="{LIGHT}"/><rect x="{x+30}" y="27" width="32" height="32" fill="{Y}"/>'
        b += t(x + 46, 92, lab, 8.5)
    b += t(215, 108, '中間四塊黃都是同一個 #F39D16。白底上看起來偏暗、偏橘，深色底上看起來更亮。', 8, fill='#444')
    return svg(430, 114, b)


# ---------- 第 12 課：版本與留白 ----------
def f_versions():
    b = ''
    vs = [('全彩・白底', '#fff', B, Y, R), ('全彩反白・深藍底', B, '#fff', Y, '#fff'), ('單色黑', '#fff', INK, INK, INK),
          ('單色白（反白）', INK, '#fff', '#fff', '#fff'), ('單色主色', '#fff', B, B, B), ('黑・放在黃上', Y, INK, INK, INK)]
    for i, (lab, bg, c1, c2, c3) in enumerate(vs):
        col, row = i % 3, i // 3
        x, y = 10 + col * 140, 8 + row * 118
        b += f'<rect x="{x}" y="{y}" width="128" height="90" fill="{bg}" stroke="{LIGHT}"/>'
        b += mark(x + 30, y + 12, 66, c1, c2, c3)
        b += t(x + 64, y + 104, lab, 8.5)
    b += t(215, 246, '練習用形狀，不是崧淳 LOGO 提案。', 8, fill='#555')
    return svg(430, 252, b)


def f_clearspace():
    b = ''
    x, y, s = 120, 30, 100
    u = s * 0.14  # 小方塊邊長當單位
    b += f'<rect x="{x-u*1.5}" y="{y-u*1.5}" width="{s+u*3}" height="{s+u*3}" fill="none" stroke="{R}" stroke-dasharray="4 3" stroke-width="0.8"/>'
    b += mark(x, y, s, INK, INK, INK)
    b += f'<rect x="{x-u*1.5}" y="{y+s/2-u/2}" width="{u}" height="{u}" fill="none" stroke="{R}" stroke-width="0.8"/>'
    b += t(x - u * 1.5 - 4, y + s / 2 + 3, '1 單位', 7.5, 'end', R)
    b += t(x + s / 2, y + s + u * 1.5 + 16, '留白：四周至少 1.5 個「小方塊」寬，這個範圍內不放別的字或圖。', 8, fill='#444')
    # 最小尺寸
    b += f'<g transform="translate(330,60)">{mark(0,0,40,INK,INK,INK)}</g>' + t(350, 116, '印刷最小 15 mm 寬', 7.5)
    b += f'<g transform="translate(400,72)">{mark(0,0,16,INK,INK,INK)}</g>' + t(408, 104, '螢幕 16 px', 7.5)
    return svg(440, 190, b)


# ---------- 第 13 課：流程 ----------
def f_flow():
    steps = ['一頁簡報', '同行牆＋查撞標', '30 格黑白剪影', '三測篩到 3 個', '格線＋視覺修正', '縮小／單色／反白', '上色（1–2 色）', '五個版本', '檢查表自評', '提案：黑白→彩色']
    b = ''
    for i, s in enumerate(steps):
        col, row = i % 5, i // 5
        x, y = 8 + col * 86, 10 + row * 60
        b += f'<rect x="{x}" y="{y}" width="76" height="34" rx="3" fill="#f4f4f4" stroke="{MID}"/>'
        b += t(x + 6, y + 13, str(i + 1), 8, 'start', '#777', 700)
        b += t(x + 38, y + 24, s, 7.4)
        if col < 4:
            b += f'<path d="M{x+77},{y+17} L{x+85},{y+17}" stroke="{INK}" stroke-width="1"/><path d="M{x+85},{y+17} l-3,-2.5 v5 z" fill="{INK}"/>'
    b += f'<path d="M{8+4*86+38},{44} C{8+4*86+38},{58} {46},{52} {46},{66}" stroke="{INK}" fill="none" stroke-width="1"/><path d="M{46},{70} l-2.5,-4 h5 z" fill="{INK}"/>'
    return svg(440, 108, b)


# ---------- 練習用形狀：縮小測試原稿（給 render 用） ----------
def raw_thin(s=128):
    r = s * 0.4
    o = f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}"><rect width="{s}" height="{s}" fill="#fff"/>'
    for k, rr in enumerate([r, r * 0.8, r * 0.6]):
        o += f'<circle cx="{s/2}" cy="{s/2}" r="{rr}" fill="none" stroke="#000" stroke-width="{s*0.018}"/>'
    o += f'<line x1="{s*0.1}" y1="{s/2}" x2="{s*0.9}" y2="{s/2}" stroke="#000" stroke-width="{s*0.018}"/>'
    o += f'<circle cx="{s/2}" cy="{s/2}" r="{s*0.05}" fill="#000"/></svg>'
    return o


def raw_bold(s=128):
    r = s * 0.36
    w = s * 0.11
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}"><rect width="{s}" height="{s}" fill="#fff"/>'
            f'<circle cx="{s/2}" cy="{s/2}" r="{r}" fill="none" stroke="#000" stroke-width="{w}"/>'
            f'<rect x="{s*0.12}" y="{s/2-w/2}" width="{s*0.76}" height="{w}" fill="#000"/></svg>')


def raw_four(s=128, gap=0.04):
    q = s * (0.8 - gap) / 2
    g = s * gap
    o = f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}"><rect width="{s}" height="{s}" fill="#fff"/>'
    for dx in (0, 1):
        for dy in (0, 1):
            o += f'<rect x="{s*0.1+dx*(q+g)}" y="{s*0.1+dy*(q+g)}" width="{q}" height="{q}" fill="#000"/>'
    return o + '</svg>'


ALL = dict(system=f_system, types=f_types, gestalt=f_gestalt, silhouette=f_silhouette, negative=f_negative,
           optical=f_optical, construct=f_construct, reverse=f_reverse, values=f_values, wheel=f_wheel,
           ncolours=f_ncolours, proportion=f_proportion, cvd=f_cvd, albers=f_albers, versions=f_versions,
           clearspace=f_clearspace, flow=f_flow)
