"""把 資料/ 裡的 JSON 組成手機頁（../配色參考庫.html）。只用標準函式庫。
用法：python3 build_page.py
"""
import json, os, sys, html, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from colormath import oklch, contrast, from_oklch, max_chroma

D = os.path.join(HERE, '..', '資料')
e = html.escape


def J(name, default=None):
    p = os.path.join(D, name)
    return json.load(open(p)) if os.path.exists(p) else default


def ink(h):
    return '#111' if contrast(h, '#111111') >= contrast(h, '#FFFFFF') else '#fff'


def chip(h, label=None, size='m'):
    lab = e(label) if label else h.upper()
    return f'<span class="chip {size}" style="background:{h};color:{ink(h)}"><code>{lab}</code></span>'


def strip(hexes, cap=''):
    cells = ''.join(f'<i style="background:{h};flex:1"></i>' for h in hexes)
    codes = ' '.join(h.upper() for h in hexes)
    return f'<figure class="strip"><div class="bar">{cells}</div><figcaption><code>{e(codes)}</code>{(" · " + cap) if cap else ""}</figcaption></figure>'


def section(id_, kicker, title, body):
    return f'<section id="{id_}"><p class="kicker">{e(kicker)}</p><h2>{e(title)}</h2>{body}</section>'


# ---------- 名家與人氣配色 ----------
def sec_palettes():
    r = J('冷深色加黃_名家與人氣配色.json')
    order = ['藍', '青', '青綠', '綠']
    out = []
    w, c = r['wada'], r['colourlovers']
    out.append('<p class="lead">和田三造《配色事典》348 組裡有 <b>%d 組</b>、COLOURlovers 人氣前 992 組裡有 <b>%d 組</b>，同時含「冷深色」和「亮黃」。下面全部列出，依冷色分四類。</p>' % (w['hits'], c['hits']))
    out.append('<div class="facts">'
               '<div><b>6 / 73</b><span>第三色只用灰白，或沒有第三色。但資料庫本來就少用灰白（和田 3 色組 27%%、人氣 17%%），樣本又小，不是規律</span></div>'
               '<div><b>%s · %s</b><span>第三色含紅、珊瑚、赭這類暖色（和田 · 人氣）。整個資料庫本來就約 75%% 的配色有暖色，冷＋黃沒有特別偏好</span></div>'
               '<div><b>L %.2f · C %.2f</b><span>冷深色的中位明度、彩度（OKLCH，和田）。人氣組 L %.2f · C %.2f</span></div>'
               '</div>' % (w['third_group_share']['暖紅系（紅、珊瑚、紅褐、橘、棕、粉）'], c['third_group_share']['暖紅系（紅、珊瑚、紅褐、橘、棕、粉）'],
                          w['median']['cool_L'], w['median']['cool_C'], c['median']['cool_L'], c['median']['cool_C']))
    for src, data, label in (('wada', w, '和田三造《配色事典》'), ('colourlovers', c, 'COLOURlovers 人氣')):
        out.append(f'<h3>{label}</h3>')
        groups = collections.defaultdict(list)
        for p in data['palettes']:
            groups[p['cool_sub']].append(p)
        for g in order:
            if not groups[g]: continue
            out.append(f'<p class="sub">冷色是「{g}」的 {len(groups[g])} 組</p><div class="grid-strips">')
            for p in groups[g]:
                names = ' / '.join(x.get('name', '') for x in p['colors']) if src == 'wada' else ''
                cap = f'#{p["id"]}' + (f' {e(names)}' if names else '')
                out.append(strip([x['hex'] for x in p['colors']], cap))
            out.append('</div>')
    return section('palettes', '開源色庫', '名家與人氣配色裡的冷深色＋黃', ''.join(out))


# ---------- 擁擠度 ----------
def sec_crowding():
    d = J('全球品牌冷色擁擠度.json')
    grid = d['grid']
    hues = sorted(set(g['hue_from'] for g in grid))
    Ls = sorted(set(g['L_from'] for g in grid), reverse=True)
    name = {140: '綠', 155: '綠', 170: '青綠', 185: '青綠', 200: '青', 215: '青', 230: '藍', 245: '藍', 260: '深藍'}
    cells = ['<div class="hm-corner">明度</div>'] + [f'<div class="hm-h">{name[h]}<small>{h}°</small></div>' for h in hues]
    for L in Ls:
        cells.append(f'<div class="hm-l">{L:.1f}</div>')
        for h in hues:
            g = next(x for x in grid if x['hue_from'] == h and x['L_from'] == L)
            Lm, Hm = L + 0.05, h + 7.5
            col = from_oklch(Lm, min(0.12, max_chroma(Lm, Hm) * 0.85), Hm)
            n = g['global_count']; tw = g['taiwan_peers']
            title = e('、'.join(g['global_examples'][:5]) + ((' ｜台灣同業：' + '、'.join(tw)) if tw else ''))
            cells.append(f'<div class="hm-c" style="background:{col};color:{ink(col)}" title="{title}"><b>{n}</b>{"<i>台</i>" if tw else ""}</div>')
    body = ('<p class="lead">全球 3466 個品牌的主色（開源 simple-icons 資料庫），落在冷色區的每一格各有幾個。'
            '數字越大越擠。「台」＝台灣 14 家同業有用到這一格。</p>'
            f'<div class="scroll"><div class="hm" style="grid-template-columns:2.6em repeat({len(hues)},minmax(0,1fr))">{"".join(cells)}</div></div>'
            '<p class="note">讀法：深藍那幾格（色相 245–275°、明度 0.3–0.6）大多有 40–156 個品牌；同樣深度的綠到青（155–230°）每格 0–9 個。'
            '資料庫以科技、交通、媒體品牌為主，工程與水務很少，所以這只是這個色庫裡的粗略分布，不是同業分布，也不是台灣街頭的辨識度。</p>')
    return section('crowding', '開源品牌庫', '冷色裡哪裡擠、哪裡空', body)


# ---------- 案例（A1、A2）：精選短句，色碼從 JSON 取 ----------
A1_GROUPS = [
    ('工程機具：公司藍、機具黃', [
        ('Komatsu（小松製作所）', '小松', '藍色 logo、黃色機身，再用三條藍色條紋把兩者綁在一起。'),
        ('Volvo Construction Equipment', 'Volvo 建機', '集團藍守住企業辨識；機具塗黃，是為了和自家農機分開。'),
        ('LiuGong（柳工）', '柳工', '深藍底白字 logo 加一點橘，機具黃色。'),
        ('New Holland Construction（CNH 集團）', 'New Holland', '同一品牌：農機藍、建機黃。黃色是產品類別色，不是品牌色。'),
    ]),
    ('郵政：黃車配冷色標誌', [
        ('La Poste（法國郵政）', '法國郵政', '1962 年為雨天能見度把車改黃；藍色飛鳥負責讓人認出是誰。'),
        ('Correios（巴西郵政）', '巴西郵政', '官方手冊把藍、黃都正式命名並給齊印刷與螢幕值（藍 Pantone 540C）。手冊的黃色 RGB 寫錯，引用要自己驗算。'),
        ('Correos（西班牙郵政）', '西班牙郵政', '黃藍並重，改版只把兩色略加深。'),
        ('Poste Italiane（義大利郵政）', '義大利郵政', '萊姆黃橫條上放藍字，大家記得的是「黃底藍字」。'),
        ('Deutsche Post／DHL（對照：黃＋紅，非冷色）', '對照：DHL', '大面積黃配紅字，歐洲物流的代表色。'),
        ('Swiss Post／Die Post（對照：黃＋黑＋紅，非冷色）', '對照：瑞士郵政', '郵政黃在瑞士取得商標保護。'),
    ]),
    ('道路與能源：企業色各異，現場車都黃', [
        ('NEXCO東日本（東日本高速道路）', 'NEXCO 東日本', '企業色綠，巡邏車黃。'),
        ('NEXCO中日本（中日本高速道路）（對照：企業色橘）', 'NEXCO 中日本', '企業色橘，巡邏車一樣黃。'),
        ('NEXCO西日本（西日本高速道路）', 'NEXCO 西日本', '企業色藍，巡邏車黃。三家企業色不同、車都黃，黃是道路現場的共用色。'),
        ('ANWB（荷蘭皇家旅遊協會，含道路救援 Wegenwacht）', '荷蘭 ANWB 道路救援', '從黃色機車起家，車隊比 logo 更早成為大家的記憶點。'),
        ('Vattenfall（瑞典國營能源公司）', 'Vattenfall 能源', '藍是水與天空、黃是太陽；藍為底、黃為點。'),
    ]),
    ('深藍＋亮黃已經是誰的', [
        ('IKEA（對照：深藍＋黃大品牌）', 'IKEA', '全球家居零售。'),
        ('Lidl（對照：深藍＋黃大品牌）', 'Lidl', '歐洲平價超市，再加紅。'),
        ('Ryanair（對照：深藍＋黃大品牌）', 'Ryanair', '歐洲廉價航空。'),
        ('Best Buy（對照：深藍＋黃大品牌）', 'Best Buy', '北美 3C 量販。'),
        ('Michelin（對照：藍主色＋黃強調色）', 'Michelin', '官方設計系統：藍為主，黃只用在按鈕等重點。'),
    ]),
]

A2_GROUPS = [
    ('黃色車身已經有主人', [
        ('中華電信 工程車', '中華電信工程車', '黃色車身＋藍色圓形標誌。路人看到黃色小車配藍標，第一個想到它。'),
        ('台電（台灣電力公司）工程車', '台電工程車', '黃色工程車＋台電標誌。有人把私人小貨車漆成這樣、寫「緊急電力搶修車」來臨停。'),
        ('各縣市清潔隊垃圾車', '清潔隊垃圾車', '黃色大車沿街收運，和吸污車在同樣的巷子作業。深綠＋黃最像。'),
        ('計程車（法定純黃，含台灣大車隊等車隊）', '計程車', '整車純黃。黃色廂型車配深藍字，容易像車隊。'),
        ('公共工程工地告示牌與污水管線警示帶（國土署施工綱要規範）', '政府污水工地', '告示牌藍底白字、警示帶黃底紅字。深藍＋黃放在圍籬上，會和政府告示融在一起。'),
    ]),
    ('同業與熟悉的品牌', [
        ('銘源（同業，清溝／CCTV）', '同業 銘源', '黃色清溝車、黑色大字全名；網站深藍。'),
        ('升野（同業）', '同業 升野', '藍色管道箭頭標誌＋黃底橫幅，同業裡最明確的藍＋黃。'),
        ('宏隆（同業，清溝）', '同業 宏隆', '黃色清溝車；logo 綠色書法字＋橘色帶。'),
        ('久大管道工程（同業）', '同業 久大', 'logo 藍；網站海軍藍底＋黃色點綴。'),
        ('派浦崴洱（同業，台中）', '同業 派浦崴洱（台中）', '服務圖是黃色作業車，標誌顏色還沒查到。地區與工項都和崧淳重疊，值得追。'),
        ('IKEA 台灣', 'IKEA', '亮藍＋亮黃。'),
        ('Komatsu 小松（工程機具，國際品牌）', '小松', '藍字＋藍斜帶＋黃車身，懂工程的人一看就知道。'),
    ]),
]


def hexes_of(it):
    out = []
    for k in ('cool_primary', 'primary', 'yellow'):
        s = it.get(k)
        if isinstance(s, dict):
            for h in str(s.get('hex', '')).replace(',', ' ').split():
                if h.startswith('#') and len(h) == 7: out.append((h.upper(), s.get('grade', '')))
    for t in (it.get('third_or_neutral') or it.get('third') or []):
        if isinstance(t, dict):
            for h in str(t.get('hex', '')).replace(',', ' ').split():
                if h.startswith('#') and len(h) == 7: out.append((h.upper(), t.get('grade', '')))
    seen, uniq = set(), []
    for h, g in out:
        if h not in seen: seen.add(h); uniq.append((h, g))
    return uniq


def curated(groups, items):
    by = {it['name']: it for it in items}
    out = []
    for gname, rows in groups:
        out.append(f'<h3>{e(gname)}</h3><ul class="cases">')
        for key, label, line in rows:
            it = by[key]  # 名稱對不上就直接報錯，避免頁面和資料不一致
            hs = hexes_of(it)
            chips = ''.join(chip(h, None, 'xs') for h, _ in hs) or '<span class="nohex">色碼未取得</span>'
            grades = sorted(set(g for _, g in hs if g))
            src = [u for u in (it.get('sources') or []) if isinstance(u, str) and u.startswith('http')]
            if not src:
                src = [s.get('url') for s in (it.get('sources') or []) if isinstance(s, dict) and str(s.get('url', '')).startswith('http')]
            link = f' <a href="{e(src[0])}" rel="noopener">來源</a>' if src else ''
            g = f'<small class="grade">色碼等級 {"、".join(grades)}</small>' if grades else ''
            out.append(f'<li><div class="case-h"><b>{e(label)}</b>{g}</div><div class="chips">{chips}</div><p>{e(line)}{link}</p></li>')
        out.append('</ul>')
    return ''.join(out)


def sec_a1():
    items = J('國外_冷色識別加黃色車隊.json')
    lead = ('<p class="lead">21 個國外案例。共同點：<b>黃色多半是現場的功能色</b>，同一行業大家都用；'
            '讓人認出是哪家公司的，是冷色 logo，以及把 logo 顏色帶到黃車上的固定圖形。</p>')
    note = '<p class="note">色碼等級：A＝官方手冊或官網原文，B＝新聞或維基，C＝色碼網站或開源資料集。21 例裡色碼是 A 級的只有巴西郵政、Michelin、法國郵政（子品牌）。</p>'
    return section('fleet', '國外 21 例', '公司是冷色，車和機具是黃色', lead + curated(A1_GROUPS, items) + note)


def sec_a2():
    items = J('台灣_冷色加黃.json')
    lead = ('<p class="lead">在台灣，<b>黃色車＋藍色標誌</b>已經是中華電信、台電工程車的樣子；'
            '深綠＋黃像垃圾車和同業宏隆。深青（藍綠）＋黃這次沒找到台灣車隊在用，但沒找到不代表沒人用。</p>')
    note = '<p class="note">18 例都沒有官方色碼，車身顏色多來自新聞與第三份同業報告的文字描述。</p>'
    return section('taiwan', '台灣街頭', '冷色＋黃在台灣已經是誰的', lead + curated(A2_GROUPS, items) + note)


def sec_a3():
    items = J('設計站作品清單.json')
    if not items: return ''
    cats = collections.defaultdict(list)
    for it in items: cats[it.get('category', '其他')].append(it)
    out = ['<p class="lead">這些網站在雲端打不開，以下是從搜尋引擎索引整理的作品連結，點開就能看圖。色碼只列作品文字裡寫明的。</p>']
    for c, its in cats.items():
        out.append(f'<h3>{e(c)}（{len(its)}）</h3><ul class="refs">')
        for it in its:
            hx = ''.join(chip(h, None, 'xs') for h in it.get('hex_found', [])[:6])
            tag = it.get('commercial', '')
            out.append(f'<li><a href="{e(it["url"])}" rel="noopener">{e(it["title"])}</a> <small>{e(it.get("creator", ""))} · {e(it.get("site", ""))}{(" · " + e(tag)) if tag else ""}</small>'
                       f'<div>{hx}</div><p>{e(it.get("note", ""))}</p></li>')
        out.append('</ul>')
    return section('refs', '設計站索引', 'Pinterest、Behance 等站的相關作品', ''.join(out))


def page(sections_html, top_html):
    css = open(os.path.join(HERE, 'page.css')).read()
    return f'''<title>崧淳配色參考庫</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<style>{css}</style>
<main>{top_html}{sections_html}</main>'''


def main():
    top = open(os.path.join(HERE, 'page_top.html')).read() if os.path.exists(os.path.join(HERE, 'page_top.html')) else ''
    tail = open(os.path.join(HERE, 'page_tail.html')).read() if os.path.exists(os.path.join(HERE, 'page_tail.html')) else ''
    body = sec_a1() + sec_a2() + sec_crowding() + sec_palettes() + tail + sec_a3()
    out = os.path.join(HERE, '..', '配色參考庫.html')
    open(out, 'w').write(page(body, top))
    print('wrote', out, os.path.getsize(out))


if __name__ == '__main__':
    main()
