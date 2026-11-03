"""LOGO 設計原則統整報告：產生 report.html（再由 pdf.js 印成 A5 PDF）。
用法：python3 -I build_report.py <work 資料夾> <fonts package 資料夾> <simple-icons icons 資料夾>
"""
import base64, os, re, sys
from PIL import Image
import io

W, FONTS, SI = sys.argv[1], sys.argv[2], sys.argv[3]
IMG = os.path.join(W, 'img')
SMALL = os.path.join(W, 'small')


def read(p):
    return open(p, encoding='utf-8').read()


def strip_meta(s):
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    s = s.replace(' xmlns:c2pa="http://c2pa.org/manifest"', '')
    return s


def inline_svg(name, cls='fig'):
    s = strip_meta(read(os.path.join(IMG, name)))
    s = re.sub(r'<svg ', f'<svg class="{cls}" ', s, count=1)
    s = re.sub(r' width="[0-9.]+" height="[0-9.]+"', '', s, count=1)
    return s


def img_svg(path, style=''):
    s = strip_meta(read(path))
    d = base64.b64encode(s.encode('utf-8')).decode()
    return f'<img style="{style}" src="data:image/svg+xml;base64,{d}">'


def si(name, size='64px', fill='#111111'):
    s = read(os.path.join(SI, name + '.svg'))
    s = re.sub(r'<title>.*?</title>', '', s)
    s = s.replace('<svg ', f'<svg style="width:{size};height:{size}" fill="{fill}" ', 1)
    return s


def img_png(path, style='', maxw=None):
    im = Image.open(path)
    if maxw and im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'PNG', optimize=True)
    return f'<img style="{style}" src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}">'


def small(name, h):
    return img_png(os.path.join(SMALL, f'big_{name}_{h}.png'), 'height:20mm;image-rendering:pixelated')


V = '<span class="t bad">違反</span>'
P = '<span class="t part">部分</span>'
O = '<span class="t ok">符合</span>'
N = '<span class="t na">無</span>'
U = '<span class="t na">未比對</span>'

# ---------- 圖 ----------
FIG_G1 = f'''<figure><div style="width:78%;margin:0 auto">{inline_svg('G1_annot.svg')}</div>
<figcaption>圖 1　G1 白底版。虛線框：左邊的符號「山」，和崧字上半本來就有的「山」。三個元素一樣大、一樣粗、同一個顏色，整排讀成「山崧淳」。</figcaption></figure>'''

FIG_IDOT = f'''<figure class="row">
<div class="cell" style="width:32%">{inline_svg('G1_idot.svg')}</div>
<div class="cell" style="width:52%">{inline_svg('G2_white.svg')}<div class="reading">讀起來是：山崧淳.</div></div>
<figcaption>圖 2　左：G1 中間豎條加上方一格紅，跟小寫 i 是同一個結構（一根豎、上面一點）。右：G2 底線尾端的紅格，在一排字後面就是句點。</figcaption></figure>'''

FIG_G3 = f'''<figure class="row">
<div class="cell" style="width:30%">{inline_svg('G3_white.svg', 'figs3')}<div class="lab">Claude 向量稿</div></div>
<div class="cell" style="width:40%">{img_png(os.path.join(IMG, 'G3_v4.png'), 'height:42mm', 520)}<div class="lab">AutoIP v4：崧被拆成「山」加完整的「松」</div></div>
<figcaption>圖 3　G3 直排方印兩個版本。</figcaption></figure>'''

def lab_img(html, label, w):
    return f'<div class="cell" style="width:{w}"><div class="box">{html}</div><div class="lab">{label}</div></div>'

FIG_ONE = f'''<figure>
<div class="rowhead bad">一個標誌疊了三件事</div>
<div class="row">
{lab_img(img_svg(os.path.join(IMG, 'A_山水印_標誌.svg'), 'width:17mm'), '10-11 舊稿 A<br>方框＋山＋波浪', '21%')}
{lab_img(img_svg(os.path.join(IMG, 'B_通管S_標誌.svg'), 'width:17mm'), '舊稿 B<br>圓框＋S 管＋水滴', '21%')}
{lab_img(img_svg(os.path.join(IMG, 'C_山水滴_標誌.svg'), 'width:17mm'), '舊稿 C<br>水滴＋山＋水面', '21%')}
{lab_img(inline_svg('G2_white.svg', 'figs'), 'G2<br>山字＋底線＋紅格', '25%')}
</div>
<div class="rowhead ok">一個構成方法</div>
<div class="row">
{lab_img(si('mitsubishi', '17mm'), '三菱<br>同一個菱形轉三次', '30%')}
{lab_img(si('chase', '17mm'), 'Chase<br>同一塊形狀轉四次', '30%')}
</div>
<figcaption>圖 4　舊稿與 G2 每一件都要說明才知道意思；三菱、Chase 只用「重複加旋轉」一個方法，不用說明也站得住。外部標誌取自 simple-icons 16.35.0（單色版）。</figcaption></figure>'''

FIG_CHAR = f'''<figure>
<div class="rowhead bad">字排在名字旁邊</div>
<div class="row">{lab_img(inline_svg('G1_white.svg', 'figs'), 'G1：山跟崧、淳同樣大小，被當成第三個字', '60%')}</div>
<div class="rowhead ok">字畫成一個形狀</div>
<div class="row">
{lab_img(si('chinarailway', '18mm'), '中國鐵路路徽<br>人字疊在工字形鋼軌斷面上', '45%')}
{lab_img(si('jrgroup', '18mm'), 'JR<br>J、R 兩個字母連成一個形', '45%')}
</div>
<figcaption>圖 5　下排兩個標誌裡都有字，但沒有人會把它們當成一行文字讀。外部標誌取自 simple-icons 16.35.0。</figcaption></figure>'''

FIG_FRAME = f'''<figure>
<div class="row">
{lab_img(inline_svg('G3_white.svg', 'figs3b'), 'G3：藍色直排名字，同業九升已用藍色直排', '45%')}
{lab_img(si('uniqlo', '22mm'), 'UNIQLO：方框加字也能成立', '45%')}
</div>
<table class="mini"><tr><th></th><th>有完整外框</th><th>沒有外框</th></tr>
<tr><td>樣本數</td><td>597</td><td>1026</td></tr>
<tr><td>剪影跟最像的 10 個標誌的相似度</td><td>0.62</td><td>0.46</td></tr>
<tr><td>縮到 16px 保留程度</td><td>0.78</td><td>0.79</td></tr></table>
<figcaption>圖 6　上：方框本身不是問題。下：simple-icons 1623 個近方形標誌的中位數（10-17 實測）。外框讓剪影更像別人，對縮小沒有幫助。</figcaption></figure>'''

rows = ''
for name, label in [('G3', 'G3 方印'), ('G1', 'G1 橫式'), ('chinarailway', '中國鐵路'), ('mitsubishi', '三菱')]:
    rows += f'<tr><td class="l">{label}</td>' + ''.join(f'<td>{small(name, h)}</td>' for h in (96, 24, 16)) + '</tr>'
FIG_SMALL = f'''<figure><table class="sm"><tr><th></th><th>96px</th><th>24px</th><th>16px</th></tr>{rows}</table>
<figcaption>圖 7　同樣高度縮小後放大看（像素格是真的）。G3 在 24px 已讀不出字，G1 的字標 16px 只剩一條藍色；中國鐵路與三菱 16px 仍認得出輪廓。</figcaption></figure>'''

FIG_GLYPH = f'''<figure>
<div class="rowhead bad">G1 到 G3 的字：每筆同粗的直線</div>
<div class="row"><div class="cell" style="width:57mm">{inline_svg('G_glyphs.svg', 'figs')}</div></div>
<div class="rowhead ok">參考：思源黑體 Bold 的同兩個字（只看做工，不採用）</div>
<div class="row"><div class="cell notoref">崧淳</div></div>
<table class="mini"><tr><th></th><th>直筆</th><th>橫筆</th><th>橫÷直</th></tr>
<tr><td>G1 到 G3（字高 300）</td><td>24</td><td>24</td><td>1.00</td></tr>
<tr><td>思源黑體 Bold（字級 600px）</td><td>68～76</td><td>58～64</td><td>0.80～0.87</td></tr></table>
<figcaption>圖 8　上排每一筆都是同一筆寬的折線，方頭、尖角接合，撇和點沒有收筆，「子」的鉤是一段斜線。下排專業字型的橫筆比直筆細一到兩成，撇有粗細變化，點有形狀。數字是 Claude 11-03 掃描像素量的。</figcaption></figure>'''

FIG_BLEED = f'''<figure class="row">
<div class="cell" style="width:48%">{inline_svg('G1_white.svg', 'figs')}</div>
<div class="cell" style="width:48%">{inline_svg('G1_navy.svg', 'figs')}</div>
<figcaption>圖 9　兩版筆寬都是 24。白字在深藍底看起來比較粗，反白版要另外修細。</figcaption></figure>'''

# ---------- 違反對照表 ----------
TABLE_ROWS = [
    ('A1 一個標誌只放一個構成想法', P, V, O),
    ('A2 不用說明也站得住', V, V, O),
    ('A3 用字做圖形時，把字畫成形狀', V, V, N),
    ('A4 像自己，不像同行', U, U, V),
    ('A6 外框要有意義面的理由', O, P, P),
    ('A7 小尺寸要認得，或另做小尺寸版', V, V, V),
    ('B2 逐字調大小、重心、中宮、粗細', V, V, V),
    ('B3 橫細直粗、反白修細', V, V, V),
    ('B7 字要寫對', O, O, P),
    ('D2 先交黑白草圖挑方向', V, V, V),
    ('A8 圓或尖對上想傳達的屬性', O, O, O),
    ('A11 不加立體、漸層、飛線', O, O, O),
    ('C2 圖形跟名字一起出現', O, O, O),
    ('C4 顏色照實算的對比放', O, O, O),
]
TABLE = '<table class="vt"><tr><th>原則</th><th>G1</th><th>G2</th><th>G3</th></tr>' + ''.join(
    f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in TABLE_ROWS) + '</table>'

html = read(os.path.join(W, 'report_body.html'))
for k, v in dict(FIG_G1=FIG_G1, FIG_IDOT=FIG_IDOT, FIG_G3=FIG_G3, FIG_ONE=FIG_ONE, FIG_CHAR=FIG_CHAR,
                 FIG_FRAME=FIG_FRAME, FIG_SMALL=FIG_SMALL, FIG_GLYPH=FIG_GLYPH, FIG_BLEED=FIG_BLEED,
                 TABLE=TABLE, FONTS=FONTS).items():
    html = html.replace('{{' + k + '}}', v)
left = re.findall(r'\{\{[A-Z_]+\}\}', html)
assert not left, left
open(os.path.join(W, 'report.html'), 'w', encoding='utf-8').write(html)
print('report.html', len(html))
