# 產生「配色與設計理念學習報告」HTML（A5 直式，固定頁）
import json, math, html
R = '/tmp/claude-0/report/'
W = '/tmp/claude-0/work/'
naming = json.load(open(R + 'naming_fig.json'))
printd = json.load(open(R + 'print_fig.json'))
hivis = json.load(open(R + 'hivis.json'))
cand = json.load(open(R + 'candidates.json'))
schemes = json.load(open(W + 'peer_schemes.json'))

# ---------- 色彩小工具 ----------
def hex2rgb(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def enc(c):
    c = min(max(c, 0), 1); return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def Lstar(h):
    r, g, b = [lin(x) for x in hex2rgb(h)]
    Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    f = Y ** (1 / 3) if Y > (6 / 29) ** 3 else Y / (3 * (6 / 29) ** 2) + 4 / 29
    return 116 * f - 16
def grey_of(h):
    L = Lstar(h); fy = (L + 16) / 116
    Y = fy ** 3 if fy > 6 / 29 else 3 * (6 / 29) ** 2 * (fy - 4 / 29)
    v = round(enc(Y) * 255); return '#%02X%02X%02X' % (v, v, v)
def ink(h): return '#FFFFFF' if Lstar(h) < 58 else '#111111'
def oklch2hex(L, C, H):
    for k in range(60):
        a = C * math.cos(math.radians(H)); b = C * math.sin(math.radians(H))
        l_ = L + 0.3963377774 * a + 0.2158037573 * b
        m_ = L - 0.1055613458 * a - 0.0638541728 * b
        s_ = L - 0.0894841775 * a - 1.2914855480 * b
        l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
        r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
        g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
        bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
        if min(r, g, bb) >= -1e-4 and max(r, g, bb) <= 1 + 1e-4:
            return '#%02X%02X%02X' % tuple(round(enc(x) * 255) for x in (r, g, bb))
        C *= 0.95
    return '#808080'

T2T = str.maketrans('绿蓝黄红灰紫橙棕青黑', '綠藍黃紅灰紫橙棕青黑')
FAMNAME = {'蓝': '藍', '绿': '綠', '蓝绿': '藍綠', '青': '青', '黑': '黑', '灰': '灰', '紫': '紫', '橙': '橙', '黄': '黃', '棕': '棕', '红粉': '紅粉', '其他': '其他'}
FAMCOL = {'蓝': '#2F62B0', '绿': '#3C8C4C', '蓝绿': '#1E9B93', '青': '#5DB7C9', '黑': '#1A1A1A', '灰': '#9A9A9A', '紫': '#7656A8', '橙': '#E5832A', '黄': '#E1BE24', '棕': '#86593A', '红粉': '#D2455A', '其他': '#CFCFCF'}
ENFAM = {'blue': '藍', 'teal': '藍綠', 'green': '綠', 'purple': '紫', 'grey': '灰', 'black': '黑', 'orange': '橙', 'yellow': '黃', 'brown': '棕', 'pink': '粉紅', 'red': '紅', 'white': '白', 'other': '其他'}

def e(s): return html.escape(s)

# ---------- 元件 ----------
def chip(hexv, name='', size=13, show_hex=True):
    return (f'<div class="chip" style="width:{size}mm"><div class="sw" style="background:{hexv};height:{size}mm"></div>'
            f'<div class="cn">{e(name)}</div>' + (f'<div class="ch">{hexv}</div>' if show_hex else '') + '</div>')

def photo(f, cap, cls='ph'):
    return f'<figure class="{cls}"><img src="img/{f}.jpg"><figcaption>{cap}</figcaption></figure>'

pages = []
def page(body, cls=''):
    pages.append((body, cls))

# ================= 封面 =================
page(f'''
<div class="cover">
  <h1 class="ct">配色與設計理念</h1>
  <p class="cs">我這次學到的事</p>
  <p class="cm">崧淳環保科技 CIS 學習報告<br>2026 年 10 月 17 日　Claude 整理，給梁特助</p>
  <figure class="cvph"><img src="img/Tideway_c11.jpg"><figcaption>倫敦 Tideway 下水道隧道。整片灰色裡，一眼看到的只有反光橘。照片來自 Tideway 官網。</figcaption></figure>
  <p class="cn2">這是學習報告，不是配色提案。主色怎麼定，由梁特助決定；配色與設計由 GPT 主導，Claude 輔助。</p>
</div>''', 'nofoot')

# ================= 先講結論 =================
page('''
<h2>先講結論</h2>
<p class="lead">這次看了 48 家國外同業的 logo 色、121 張實景照片、Veolia 品牌手冊，讀了開源色彩知識庫，自己跑了色名、遠看、印刷三種模擬。美感串另外量了 3466 個標誌和 38 個大師作品。學到八件事：</p>
<ol class="big">
<li><b>最常見的配色是一個顏色加黑白灰。</b>48 家有 23 家這樣做，另有 7 家只用同一色系的深淺。</li>
<li><b>用兩個顏色的，會把兩色的深淺拉開。</b>19 個多色 logo，明度差中位數 32，隨機配兩色只有 17 到 20。轉成黑白還分得開，才算配得穩。</li>
<li><b>橘、黃反光衣是全行業共用的。</b>有人的照片約 71 張，約 55 張穿橘或黃反光衣，不管公司主色是什麼。暖色告訴人「這裡在施工」，說不出「這是哪一家」。</li>
<li><b>顏色要叫得出名字，才容易被記住。</b>深青被叫成「綠」和「藍」各 38%；靛藍有 68% 叫「藍」。同業 logo 主色的中位數是 88%。</li>
<li><b>遠看先丟掉顏色，明暗留得最久。</b>細線在十幾公尺外，只剩明暗差撐得住。</li>
<li><b>印在一般紙上，深色會變淺、變灰。</b>深青在非塗佈紙只剩 44% 彩度，跟黑字的色差從 12.4 掉到 5.3。</li>
<li><b>好的識別先有一件公司自己的事，再用一個顏色長年講它。</b>Vattenfall、Caterpillar、Siemens 都是這樣。</li>
<li><b>標誌只放一個想法，整套識別靠寫成數字的規則。</b>這是美感串量出來的結論，收在第二部。</li>
</ol>
<div class="toc"><b>報告分五部</b><br>一、八種配色方式　二、設計理念　三、我自己量出來的<br>四、拿深青、靛藍來檢查　五、改掉的判斷、缺口與來源</div>
''')

# ================= 一、48 家分組圖 =================
order = [('一個彩色', '一個彩色＋黑白灰'), ('兩色同色系', '同一色系的深淺'), ('三色以上', '三色以上'), ('兩色相鄰', '相鄰色'), ('兩色對比', '兩色對比'), ('只有黑白灰', '只有黑白灰')]
# Tideway 三色同屬藍綠，移到同色系；Uisce、PUB 屬相鄰色；Watercare 四色
regroup = {'Tideway': '兩色同色系', 'Uisce Éireann': '兩色相鄰', 'PUB': '兩色相鄰'}
grp = {}
for r in schemes:
    t = regroup.get(r['name'], r['t']); grp.setdefault(t, []).append(r)
def peer_chip(r):
    cols = r['cols'] or ['#FFFFFF']
    bars = ''.join(f'<div style="flex:1;background:{c}"></div>' for c in cols)
    border = ' bd' if not r['cols'] else ''
    nm = r['name'].replace('J. Murphy & Sons', 'Murphy').replace('Republic Services', 'Republic').replace('RedZone Robotics', 'RedZone').replace('東亜グラウト工業', '東亜グラウト').replace('積水化學 SPR', '積水 SPR')
    return f'<div class="pc"><div class="pcs{border}">{bars}</div><div class="pcn">{e(nm)}</div></div>'
labels = {'一個彩色': '一個彩色＋黑白灰', '兩色同色系': '同一色系深淺', '兩色相鄰': '相鄰色', '兩色對比': '兩色對比', '三色以上': '四色', '只有黑白灰': '只有黑白灰'}
blocks = ''
for key in ['一個彩色', '兩色同色系', '兩色相鄰', '兩色對比', '三色以上', '只有黑白灰']:
    rs = grp.get(key, [])
    blocks += f'<div class="grp"><div class="gl">{labels[key]}　<b>{len(rs)} 家</b></div><div class="gchips">' + ''.join(peer_chip(r) for r in rs) + '</div></div>'
page(f'''
<div class="part">一、八種配色方式</div>
<h2>先看同業實際怎麼配</h2>
<p>48 家國外同業的 logo 色，按配色方式分組。每格是一家公司 logo 裡的彩色，黑、白、灰不畫。</p>
{blocks}
<p class="cap">logo 色取自各公司官網 logo 原檔（10-17 國外同業報告素材）。「只有黑白灰」6 家的 logo 是單色黑或白，品牌色另用在網站或車上。分組是我按色相差算的：45° 以內算同色系，45° 到 90° 算相鄰，90° 以上算對比。</p>
''')

# ================= 1-1 一個顏色用到底 =================
page(f'''
<h3>1　一個顏色用到底</h3>
<p>23 家只用一個彩色，其他全是黑、白、灰。這些公司把同一個顏色用在 logo、車、制服、垃圾箱、建築上，從頭用到尾。</p>
{photo('Biffa_c13', 'Biffa（英國廢棄物）：紅車、白字，車身沒有第三個顏色。')}
{photo('Kanal-Tuerpe_c29', 'Kanal-Türpe（德國清管）：橘色窗框、橘色清淤車、橘色廂型車，整個據點同一個橘。')}
<p class="learn"><b>學到的：</b>一色為主最省事，也最好記。代價是這個顏色要一個人撐起所有場合：大面積、小字、遠看、印在紙上。第三部的實測就是在檢查這件事。</p>
''')

# ================= 1-2/1-3 同色系、相鄰 =================
def pal_row(name, cols):
    sw = ''.join(f'<div class="ps" style="background:{c}"><span style="color:{ink(c)}">{c}</span></div>' for c in cols)
    return f'<div class="prow"><div class="pn">{e(name)}</div><div class="pss">{sw}</div></div>'
mono = [('Scottish Water', ['#006FBA', '#95CAE7']), ('Insituform', ['#102E68', '#5096DC']), ('メタウォーター', ['#004697', '#6E9CD0']), ('Tideway', ['#00B398', '#52BBB3', '#7CE0D3'])]
adj = [('Sydney Water', ['#00259C', '#29ADCE']), ('Uisce Éireann', ['#0C23C6', '#00B39A', '#7FDFAE']), ('PUB 新加坡', ['#21409A', '#0172BB', '#009B8F'])]
tints = ''.join(f'<div class="ps" style="background:{c}"><span style="color:{ink(c)}">{p}</span></div>' for c, p in [('#002D62', '100%'), (oklch2hex(0.52, 0.08, 255), '70%'), (oklch2hex(0.68, 0.055, 255), '50%'), (oklch2hex(0.82, 0.03, 255), '30%')])
page(f'''
<h3>2　同一色系的深淺</h3>
<p>一個色相，一深一淺。深的寫字，淺的當底或點綴。</p>
{''.join(pal_row(n, c) for n, c in mono)}
<p>Veolia 手冊第 7 頁也這樣規定：主色盤的每個顏色可以調成 70%、50%、30% 三階。下面是用它的深藍示意（濃度是我依手冊比例模擬，不是官方色票）。</p>
<div class="prow"><div class="pn">Veolia 深藍<br>#002D62 調階</div><div class="pss">{tints}</div></div>
<h3>3　相鄰色</h3>
<p>藍配藍綠，水務公司最常見。看起來和諧，但這三家擺在一起很難分。</p>
{''.join(pal_row(n, c) for n, c in adj)}
{photo('Uisce_Eireann_c20', '愛爾蘭水務 Uisce Éireann：白車身上的藍綠標誌，人員穿藍外套。', 'ph sm')}
<p class="learn"><b>學到的：</b>同色系和相鄰色很難配錯，代價是跟同行分不開。</p>
''', 'compact')

# ================= 1-4 對比兩色 =================
pairs = [('SUEZ', '#1A1D56', '#A2C617'), ('Metro Rod', '#2E1D67', '#2EA836'), ('Roto-Rooter', '#2A1768', '#DA291C'), ('Sydney Water', '#00259C', '#29ADCE'), ('Clancy', '#D50032', '#97D700'), ('Kier', '#DA242A', '#007B86')]
def pairfig(n, a, b):
    dl = abs(round(Lstar(a) - Lstar(b)))
    return (f'<div class="pair"><div class="pt">{e(n)}</div>'
            f'<div class="pp"><div style="background:{a}"></div><div style="background:{b}"></div></div>'
            f'<div class="pp g"><div style="background:{grey_of(a)}"></div><div style="background:{grey_of(b)}"></div></div>'
            f'<div class="pd">明度差 {dl}</div></div>')
page(f'''
<h3>4　兩色對比</h3>
<p>色相差很大的兩色，例如藍配綠、藍配紅。同業的做法幾乎都是一深一亮：深色寫字，亮色做點。上排是原色，下排是轉成黑白。</p>
<div class="pairs">{''.join(pairfig(*p) for p in pairs)}</div>
<table class="t"><tr><th></th><th>明度差中位數</th><th>差 26 以上的比例</th></tr>
<tr><td>同業 19 個多色 logo</td><td>32</td><td>68%</td></tr>
<tr><td>隨機配兩個彩色</td><td>20</td><td>38%</td></tr>
<tr><td>同業 logo 色打亂重配</td><td>17</td><td>32%</td></tr></table>
<p>例外是 Kier：紅和藍綠幾乎一樣亮（明度差約 1），轉成黑白就糊成一片。樣本只有 19 個，數字當參考。</p>
<div class="two">{photo('Metro_Rod_c26', 'Metro Rod：綠車身，深藍字。')}{photo('Roto-Rooter_c04', 'Roto-Rooter：白車身，深藍底紅字。')}</div>
<p class="learn"><b>研究怎麼說：</b>Schloss 與 Palmer（2011）把「兩色好不好看」拆成三件事。色相相近，整組比較和諧；色相差大，前面的圖形比較跳出來；明暗差兩邊都有影響。（讀到的是 color-expert 的論文整理，沒讀到原文）</p>
''')

# ================= 1-5 色相環公式 =================
base = (0.53, 0.13, 250)  # Vattenfall 藍附近，只當算法示範
def sch(name, hs):
    return f'<div class="prow"><div class="pn">{name}</div><div class="pss">' + ''.join(f'<div class="ps" style="background:{oklch2hex(base[0], base[1], h % 360)}"><span style="color:#fff">{h % 360}°</span></div>' for h in hs) + '</div></div>'
page(f'''
<h3>5　色相環公式</h3>
<p>書上最常見的配色法。以一個藍為起點（OKLCH 色相 250°），各公式算出來的顏色如下。明度、彩度都固定，只換色相。</p>
{sch('互補', [250, 70])}
{sch('分裂互補', [250, 40, 100])}
{sch('三角', [250, 10, 130])}
{sch('類似', [250, 220, 280])}
<p>48 家同業沒有一家照三角或四角配。唯一四色的 Watercare，四色明度從 6 到 60，也不是照色相環排的。</p>
<p class="learn"><b>學到的：</b>色相環只告訴你用哪幾個色相，不告訴你深淺和比例，而好不好看主要看後兩者。color-expert 的說法是：配色＝幾個色相，乘上多大的對比。</p>
<p class="learn"><b>還有一件小事：</b>互補色要用感知色彩空間（OKLCH）算，靠顏色名字猜會錯。例如工程黃 #D68702 在 OKLCH 的正對面是 249° 的藍，不是紫。</p>
<p class="cap">上面的色塊是算法示範，不是建議色。</p>
''')

# ================= 1-6 依性格配色 =================
chars = [('鮮', 0.60, 0.15), ('深', 0.36, 0.08), ('灰', 0.60, 0.035), ('淺', 0.88, 0.04)]
def charrow(name, H):
    return f'<div class="prow"><div class="pn">{name}</div><div class="pss">' + ''.join(f'<div class="ps" style="background:{oklch2hex(L, C, H)}"><span style="color:{ink(oklch2hex(L, C, H))}">{c}</span></div>' for c, L, C in chars) + '</div></div>'
page(f'''
<h3>6　依性格配色</h3>
<p>同一個色相，調明暗和濃淡，氣質就換了。下面每一列色相相同，只改明度和彩度。</p>
{charrow('藍 250°', 250)}
{charrow('藍綠 200°', 200)}
{charrow('橘黃 70°', 70)}
<p><b>研究怎麼說：</b>Ellen Divers 的研究結論是，人對顏色的情緒反應，主要看彩度和明度，色相影響比較小；一組低彩度的顏色，換哪個色相都偏沉穩。（color-expert 轉述，單一來源）</p>
<p><b>定位：</b>折扣、速食、量販多用最鮮的原色，求快、求注意；高價品牌多用低彩度、配一個克制的重點色。顏色太多、對比太強，反而顯得便宜。（color-expert 收錄的影片整理，可信度低，只當線索）</p>
<p class="learn"><b>學到的：</b>先決定要「鮮、深、灰、淺」哪一種氣質，再選色相。下水道清淤是工程服務，同業主色多落在「深」和「鮮」兩格。</p>
<p class="learn"><b>注意橘黃那一列：</b>橘黃調深就變成褐色。第三部會講到，暗黃、褐色是人最不喜歡的顏色之一。</p>
<p class="cap">「同業多落在深和鮮」是我看第 3 頁分組圖的目視歸納。</p>
''')

# ================= 1-7 比例 =================
page(f'''
<h3>7　比例：誰當主角</h3>
<p>同一組顏色，比例不同，看起來是兩家公司。常見的經驗法則是 60、30、10：一個顏色佔大面積，一個輔助，一個點綴，避免三個顏色搶戲（color-expert）。</p>
<div class="two">{photo('Thames_Water_c01', 'Thames Water：白色領頭，藍只在 logo 和字。')}{photo('Biffa_c02', 'Biffa：紅色領頭，白只在字。')}</div>
{photo('iPEK_c12', 'iPEK（德國管內檢視）：橘、白斜切對半。官網渲染圖，不是實拍。', 'ph sm')}
<p>Vattenfall 的官方品牌說明把白色放第一位，理由是給眼睛空間、清楚（10-16 筆記）。Veolia 手冊第 7 頁建議：同一頁、同一張圖最多用兩個顏色，另外可加黑、白。它的色盤除了紅白黑還有 14 色，但同一個畫面只建議用兩色。</p>
<p class="learn"><b>學到的：</b>色盤可以大，同一個畫面要少。比例要先定，才知道主色是大面積用還是小面積用，這會影響主色該多深、多鮮。</p>
''')

# Veolia 手冊頁
page('''
<h3>Veolia 手冊原頁：色票怎麼寫（第 7 頁）</h3>
<figure class="ph full"><img src="img/veolia_p7_palette.jpg"><figcaption>紅、白、黑是固定三色。下面 7 個主色可調成 70%、50%、30%；再下面 7 個淺色。右欄 Combinations：同一頁、跨頁或同一張圖，建議最多兩色，可另加黑、白。</figcaption></figure>
<p>右欄還寫了一件事：主色「適合放字，保證好讀」；淺色「不保證好讀」。也就是說，色票本身就分好了哪些顏色能放字、哪些只能當底或裝飾。</p>
<p class="learn"><b>學到的：</b>色票不只列顏色，還要寫清楚每個顏色能做什麼：能不能放字、能調幾種深淺、一次最多用幾個。</p>
<p class="cap">取自 Veolia 公開的《The Essentials of the Graphic Charter》（2024 年 3 月版），10-17 國外同業報告素材。</p>
''')
page('''
<h3>Veolia 手冊原頁：logo 只有一個顏色（第 3 頁）</h3>
<figure class="ph full"><img src="img/veolia_p3_colour.jpg"><figcaption>右上 Colors：Veolia 的 logo 是紅色；白、黑只在合作案等非用不可的場合例外。下面 Don'ts 第一格：不准用紅以外的顏色或別的字體。</figcaption></figure>
<p>同一頁還寫：標誌和名字不能拆開；四周留白等於字母 V 的寬度；橫式為主，直式只在空間不夠時用。</p>
<p>每個顏色都給四套數字：印刷用 Pantone 和 CMYK，螢幕用 RGB 和 HEX。</p>
<p class="learn"><b>學到的：</b>主色定一個就不再換，連黑白版都寫成例外。只給 HEX 不夠，印出來會走樣，第三部有實測。</p>
''')

# ================= 1-8 招牌色＋共用訊號色 =================
hv = [(k, v) for k, v in hivis.items() if v['share'] > 0.02]
hvs = ''.join(f'<div class="chip" style="width:14mm"><div class="sw" style="background:{v["hex"]};height:10mm"></div><div class="cn">{k.split("_c")[0].replace("_", " ")}</div><div class="ch">{v["hex"]}</div></div>' for k, v in hv)
hvs += '<div class="chip" style="width:14mm"><div class="sw" style="background:#D68702;height:10mm;outline:1.2pt solid #111"></div><div class="cn">工程黃</div><div class="ch">#D68702</div></div>'
page(f'''
<h3>8　招牌色，加上共用的訊號色</h3>
<p>我逐張看了 121 張實景照。有人的約 71 張，約 55 張穿橘色或螢光黃反光衣。公司主色是紅、藍、綠、粉紅都一樣，大家把 logo 印在反光衣上。</p>
<div class="six">{photo('Biffa_c01', 'Biffa 紅')}{photo('Kier_c08', 'Kier')}{photo('SUEZ_c01', 'SUEZ')}{photo('Metro_Rod_c16', 'Metro Rod')}{photo('Lanes_Group_c01', 'Lanes 粉紅')}{photo('Clancy_c31', 'Clancy')}</div>
<p>從照片量反光衣的顏色（螢光色超出螢幕色域，只是近似）：</p>
<div class="hv">{hvs}</div>
<p>反光橘偏紅（OKLCH 色相 38 到 55），反光黃偏綠（117 到 123），車身工程黃在中間（69）。工程黃跟最接近的反光橘差 11（ΔE2000），看得出不同，但屬於同一族「施工的暖色」。</p>
<p class="learn"><b>學到的：</b>暖色訊號色是全行業共用的，它說「這裡在施工」，不說「這是崧淳」。Romaniuk（品牌資產研究）說，跟別人共用的元素比較弱。認出是哪一家，要靠招牌色。</p>
<p class="cap">「約 71 張、約 55 張」是我目視數的，計數規則：照片裡看得到工作人員就算有人。</p>
''')

# 另一種做法：品牌色做進制服
page(f'''
<h3>另一種做法：把招牌色做進制服</h3>
<p>也有同業不靠反光背心，而是整套品牌色工作服，或把品牌色做進反光衣。這時候工作人員本身就是招牌。</p>
<div class="two">{photo('Metawater_c09', 'メタウォーター（日本）：藍色制服、白安全帽。官網形象圖。')}{photo('Kaiser_c23', 'KAISER（列支敦斯登）：深藍工作服。')}</div>
<div class="two">{photo('Roto-Rooter_c01', 'Roto-Rooter（美國）：全員藍條紋制服，白車一字排開。')}{photo('Tideway_c05', 'Tideway（英國）：橘、青綠兩色反光工作服，配粉紅安全帽。')}</div>
<p class="learn"><b>學到的：</b>顏色出現在哪裡，跟選什麼顏色一樣重要。同業用招牌色的地方，常見的有車、制服、垃圾箱、圍籬、建築、文件。崧淳車身已定，這份報告不談車。</p>
''')

# ================= 二、設計理念 =================
page(f'''
<div class="part">二、設計理念</div>
<h3>1　一個顏色，講一件公司自己的事</h3>
<p><b>Vattenfall（瑞典電力）</b>：藍是水和天空，黃是太陽，白領頭。2018 年改版前調查 3000 多人，發現舊顏色跟同業分不開；新標誌黃在上、藍在下，代表一代人內淘汰化石燃料。（10-16 筆記）</p>
<p><b>Caterpillar</b>：黃色是為了讓道路工地被看見而選的。先決定顏色要做什麼事，再挑色。（10-13 筆記）</p>
<p><b>Veolia</b>：手冊第 3 頁寫，紅色雙圓是一個人用頭和雙臂抱住地球；紅色抓住注意、表現活力。（原文已讀）</p>
<p><b>Siemens 石油青</b>：沿用多年，Siemens 家電依歷史微調過，沒有換掉。小松的藍沒有官方意義，靠一直用。（10-16 筆記）</p>
<div class="chips">{chip('#2071B5', 'Vattenfall 藍')}{chip('#FFDA00', 'Vattenfall 黃')}{chip('#FFCD11', 'Caterpillar 黃')}{chip('#E52028', 'Veolia 紅')}{chip('#009999', 'Siemens 石油青')}</div>
<p class="learn"><b>學到的：</b>站得住的理由，是公司自己的目標或工作需要。我前幾輪用「崧」字裡有山、「淳」字有水當配色理由，是拿名字做文字遊戲，不是公司的事。</p>
''')

page(f'''
<h3>2　跟同業反著走</h3>
<p>48 家同業裡，23 家的 logo 主色是藍；10-17 國外同業報告把紫藍也算進去，是 26 家。少數幾家刻意用別的顏色，而且用到底。</p>
<div class="two">{photo('Lanes_Group_c31', 'Lanes Group：清淤車和廂型車都是粉紅。')}{photo('Metro_Rod_c19', 'Metro Rod：綠色吸污車，同業裡很少見。')}</div>
<p class="sub">同一個行業的「藍色大隊」：</p>
<div class="three">{photo('Republic_Services_c06', 'Republic Services')}{photo('Cleanaway_c01', 'Cleanaway')}{photo('Kaiser_c03', 'KAISER')}</div>
<p class="learn"><b>學到的：</b>Romaniuk 的說法是「好認，就是長得像自己、不像別人」。反著走的公司都用整套到底：車、制服、垃圾箱一起換，只換 logo 沒有用。</p>
<p class="learn"><b>但空位要付代價：</b>沒人用的顏色，常常是有原因的。第三、四部會看到，深青附近的空位，部分來自它難叫名、印刷弱。</p>
''')

long_brands = [('Tiffany 藍', '#81D8D0'), ('Caterpillar 黃', '#FFCD11'), ('John Deere 綠', '#367C2B'), ('DHL 黃', '#FFCC00'), ('Siemens 石油青', '#009999'), ('IKEA 藍', '#0058A3')]
page(f'''
<h3>3　長年用同一個精確的顏色</h3>
<div class="chips">{''.join(chip(h, n) for n, h in long_brands)}</div>
<p>這些顏色被認得，靠的是幾十年不換。Romaniuk 的研究建議：品牌資產建立期間不要一直改，否則等於同時在養好幾個不同的資產。她的團隊也發現，行銷人員憑直覺判斷自家資產強不強，常常不準，要問消費者才算數。（訪談與報導摘要）</p>
<p><b>記憶也會偏：</b>Bae 等人（2015）的實驗發現，人記住的顏色會被拉向類別的中心，離開類別邊界。也就是說，記憶會把顏色存成「藍」或「綠」再加一點細節。（只讀到摘要）</p>
<p class="learn"><b>學到的：</b>一個卡在兩個類別中間的顏色，很容易被記成旁邊的典型色。Tiffany 藍、Siemens 石油青也卡在藍綠之間，它們用專屬名字和幾十年的一致，補回這個弱點。</p>
''')

# 美感串：標誌
page('''
<h3>4　標誌只放一個想法（美感串）</h3>
<p>美感串看了 Logo Archive 38 個 1960 到 80 年代的標誌：33 個只用一個構成方法，例如重複、旋轉、同一塊形狀兩種讀法；沒有一個疊三樣東西。我們 10-11 的三個舊稿，每個都疊了三樣。</p>
<figure class="ph full"><img src="img/aes1_one.png"></figure>
<p class="learn"><b>學到的：</b>先決定用哪一個構成方法，再談要不要放行業的東西。Rand 說標誌很少在描述業務，意義是公司做事做出來以後才累積上去的；Bierut 說標誌是等待意義的空容器。（10-13 筆記）</p>
''')

page('''
<h3>5　外框和細線（美感串）</h3>
<figure class="ph full"><img src="img/aes1_frame.png"></figure>
<figure class="ph full"><img src="img/aes1_thin.png"></figure>
<p class="learn"><b>學到的：</b>外框不會讓標誌縮小更好認，只會讓它變成一個圓或一個方塊。最細的線和縫隙不低於標誌寬度的 1/14，做不到就另畫小尺寸版本。量測只能當及格線，大師作品在這些量測上落在一般標誌的中間，好不好看還是要看圖。</p>
''')

page('''
<h3>6　整套識別靠規則（美感串）</h3>
<figure class="ph full"><img src="img/aes2_nasa.png"></figure>
<p class="learn"><b>學到的：</b>顏色不能改的時候，靠位置、尺寸、明暗反轉的規則，把不同的東西串成一套。規則要寫成數字，才守得住。</p>
''')
page('''
<h3>7　組合方式要限定（美感串）</h3>
<figure class="ph full"><img src="img/aes2_br.png"></figure>
<p class="learn"><b>學到的：</b>一個標誌只准幾種排法、幾個顏色。British Rail 只准四種排法、紅黑白三色；Veolia 同一頁最多兩色。顏色越少，規則越容易守。</p>
''')

page('''
<h3>8　公用事業這十年怎麼改版（美感串）</h3>
<figure class="ph full"><img src="img/aes2_rebrand.png"></figure>
<p class="learn"><b>學到的：</b>比較一致的方向只有一個：拿掉飛線、斜體、照片效果。圖形去留沒有一致方向，所以「改成只用名字」不能說成趨勢。</p>
''')
page('''
<h3>9　交件版面的 AI 感（美感串）</h3>
<figure class="ph full"><img src="img/aes2_ai.png"></figure>
<p class="cap">這份報告照這條改了：白底、不用米色底、不用間隔號、不拉開字距。字型只有雲端裝好的文泉驛正黑，開源中文字型的下載還在等你同意。</p>
''')

# ================= 三、我自己量出來的 =================
def namerow(d):
    bars = ''
    for k, v in d['zh'].items():
        if v < 0.02: continue
        lab = FAMNAME.get(k, k) if v >= 0.09 else ''
        bars += f'<div style="width:{v * 100:.1f}%;background:{FAMCOL.get(k, "#ccc")};color:{ink(FAMCOL.get(k, "#ccc"))}">{lab}</div>'
    top = '、'.join(f'{n.translate(T2T)} {round(p * 100)}%' for n, p in d['zh_names'][:2])
    en = d['en']; ek = list(en.items())[0]
    return (f'<div class="nr"><div class="nsw" style="background:{d["hex"]}"></div><div class="nb"><div class="nn">{e(d["name"])} <span>{d["hex"]}</span></div>'
            f'<div class="bar">{bars}</div><div class="nt">最常見叫法：{top}。英文 {round(ek[1] * 100)}% 叫{ENFAM.get(ek[0], ek[0])}。</div></div></div>')
page(f'''
<div class="part">三、我自己量出來的</div>
<h3>1　叫得出名字嗎</h3>
<p>用公開的大型色名問卷資料，看每個顏色附近的人怎麼叫它。長條是中文受試者歸到哪個色系的比例。</p>
{''.join(namerow(d) for d in naming)}
<p class="cap">中文：uwdata 多語色名資料（Kim、Thayer、Gorsky、Heer，EuroVis 2019），取 OKLab 最近的 60 筆回答，簡體字我轉成繁體。英文：Heer 與 Stone（CHI 2012）的 XKCD 色名模型。都是網路問卷，受試者沒有分台灣、中國；不是真人辨識測試。</p>
''')

page('''
<h3>叫名字的基準</h3>
<table class="t"><tr><th>哪一群顏色</th><th>中文最多人歸的色系，中位數</th></tr>
<tr><td>國外同業 42 個彩色 logo 主色</td><td>88%</td></tr>
<tr><td>台灣 17 家同業主色</td><td>90%</td></tr>
<tr><td>長年單色品牌 12 個</td><td>88%</td></tr>
<tr><td>隨機的深色彩色（明度 25 到 45）</td><td>82%</td></tr>
<tr><td><b>深青 #0C424A</b></td><td><b>38%（綠、藍各半）</b></td></tr>
<tr><td><b>靛藍 #333D66</b></td><td><b>68%（藍）</b></td></tr></table>
<p>81 個顏色裡，深青的英文色系一致度最低（38%），比 Tiffany 藍（50%）還低。台灣同業華通衛生行的深青綠 #005959 也卡在邊界（50%）。</p>
<p>工程黃 #D68702 中文最常叫「土黃色」，色系是黃 52%、橙 40%，也在邊界上。</p>
<p class="learn"><b>學到的：</b>叫不出名字的顏色，客戶轉述時會說成「綠色那家」或「藍色那家」，記憶也會往典型色偏（Bae 2015）。這不代表不能用，但要靠更長的一致和一個專屬名字補。</p>
<p class="learn"><b>為什麼這件事以前沒看到：</b>我以前只量色碼、色差和對比，三個數字都正常，色名這一關沒量過。</p>
''')

page('''
<h3>2　越遠，越看不出顏色</h3>
<figure class="ph full"><img src="img/fig_distance.png"></figure>
<p>人眼對明暗的解析度比對顏色高。用 S-CIELAB（Zhang 與 Wandell 1996）模擬：工程黃細線放在四種底色上，越遠越看不出黃，只剩「比底亮多少」。</p>
<table class="t"><tr><th>底色</th><th>14 公尺外，黃線對底的亮度比</th></tr>
<tr><td>深青 #0C424A</td><td>3.0</td></tr><tr><td>靛藍 #333D66</td><td>2.9</td></tr>
<tr><td>中藍 #2071B5（Vattenfall）</td><td>1.7</td></tr><tr><td>石油青 #009999（Siemens）</td><td>1.2，幾乎消失</td></tr></table>
<p class="learn"><b>學到的：</b>主色和輔色要靠明暗差分開，不能靠色相差。深青、靛藍都夠深，黃線在遠處還是一條比較亮的米灰線；中明度的藍和青，黃線會不見。10-16 用 AutoIP 生圖看到「琥珀線在石油青上糊掉」，這次有了原因。</p>
<p class="cap">模擬參數用 1996 原始發表值（ISETCam 收錄）。近距離那格的光暈是濾波造成的，比真實誇張。螢幕色，不代表實物。</p>
''')

def prow3(name, key, note=''):
    d = printd[key]
    cells = ''
    for c in ['螢幕', '銅版紙', '非塗佈紙']:
        v = d[c]['view']; tx = printd['黑字墨灰'][c]
        cells += (f'<div class="pc3"><div class="pbox" style="background:{v}"><span style="background:{tx};"></span></div>'
                  f'<div class="pnum">彩度 {d[c]["C"]}<br>對黑字 {d[c]["de_text"]}</div></div>')
    return f'<div class="pr3"><div class="pn">{name}<br><span>{note}</span></div>{cells}</div>'
page(f'''
<h3>3　印在紙上</h3>
<p>同一個色碼，印在銅版紙和一般非塗佈紙（影印紙、信封、便條）上會不一樣。我用公開的印刷特性資料（FOGRA39 銅版、FOGRA47 非塗佈）推估最接近的印法。色塊中間的小方塊是黑字墨色。</p>
<div class="pr3 hd"><div class="pn"></div><div class="pc3">螢幕</div><div class="pc3">銅版紙</div><div class="pc3">非塗佈紙</div></div>
{prow3('深青', '深青', '#0C424A')}
{prow3('靛藍', '靛藍', '#333D66')}
{prow3('工程黃', '工程黃', '#D68702')}
{prow3('華通深青綠', '華通衛生行', '#005959')}
{prow3('Vattenfall 藍', 'Vattenfall藍', '#2071B5')}
<table class="t"><tr><th>非塗佈紙上</th><th>彩度剩下</th><th>跟黑字的色差</th></tr>
<tr><td>深青</td><td>44%</td><td>從 12.4 掉到 5.3</td></tr>
<tr><td>靛藍</td><td>68%</td><td>從 18.3 掉到 15.7</td></tr>
<tr><td>工程黃</td><td>68%</td><td>往土黃、米色偏</td></tr></table>
<p class="cap">數字是 CIEDE2000 色差；「對黑字」是主色跟黑字墨色的色差，越小越分不開。這是模型推估，不是打樣，正式定色要實體印樣。</p>
''')

page('''
<h3>印刷學到的</h3>
<p class="learn"><b>非塗佈紙最深只印得到明度約 27（模型推估），</b>比深青、靛藍本身還淺。所以很深的主色印在一般紙上，會被抬亮、變灰。</p>
<p class="learn"><b>深青受影響最大：</b>它的彩度本來就低（18），印在一般紙上剩 8，跟黑字只差 5.3，名片上的深青字和黑字會像同一個顏色。靛藍彩度高一些，保留得比較好。</p>
<p class="learn"><b>工程黃會往土黃偏：</b>非塗佈紙上的工程黃推估是 #D4974F。Palmer 與 Schloss（2010）的研究發現，暗黃、橄欖、褐色是人最不喜歡的顏色之一，因為讓人聯想到腐爛和排泄物（只讀到摘要）。下水道行業特別要避開這個聯想，工程黃不宜再調深。</p>
<p class="learn"><b>所以手冊要寫兩套印刷色：</b>銅版用一個 Pantone C，非塗佈用另一個 Pantone U，各自打樣確認。Veolia 每個顏色都同時給 Pantone、CMYK、RGB、HEX。</p>
<h3>4　其他研究（只讀到摘要或整理稿）</h3>
<p><b>面積越大，看起來越亮、越鮮。</b>CIE 208:2014 報告：大面積色塊在實驗室裡看起來明度、彩度都比小色票高，色相也會偏。所以小色票選的顏色，刷成整面牆會比預期搶眼。</p>
<p><b>冷色那一邊分得比較粗。</b>Koenderink 等人 2026 年的預印本：螢幕色彩大約只分得出一千個「明顯不同」的區域，藍、青、綠那半邊的格子比紅、黃那半邊大。也就是冷色之間，要拉更大的差距才看得出不同。（color-expert 論文整理，預印本未經同儕審查）</p>
''')

# ================= 四、拿深青、靛藍來檢查 =================
page(f'''
<div class="part">四、拿深青、靛藍來檢查</div>
<p>用前面學到的規則，把兩個主色候選並排比較。只列事實，不做推薦。</p>
<div class="cmp"><div></div><div class="cmh"><div class="cms" style="background:#0C424A"></div>深青 #0C424A</div><div class="cmh"><div class="cms" style="background:#333D66"></div>靛藍 #333D66</div>
<div class="cml">叫得出名字</div><div>綠 38%、藍 38%，81 色中最低</div><div>藍 68%，英文藍 79%</div>
<div class="cml">附近的同業</div><div>色差 10 以內 1 家：華通衛生行 9.3（台灣）。國外最近 Ventia 16.7</div><div>色差 10 以內 5 家：Insituform 6.7、大亞 7.4（台灣）、Rioned 7.5、KAISER 8.6、PUB 9.4</div>
<div class="cml">遠看黃線</div><div>14 公尺外亮度比 3.0</div><div>14 公尺外亮度比 2.9</div>
<div class="cml">非塗佈紙</div><div>彩度剩 44%，跟黑字差 5.3</div><div>彩度剩 68%，跟黑字差 15.7</div>
<div class="cml">配工程黃</div><div>對比 3.9，明度差 38</div><div>對比 3.7，明度差 36</div>
<div class="cml">白字在上面</div><div>對比 11.1</div><div>對比 10.5</div></div>
<p class="learn"><b>看得出的取捨：</b>深青比較少人用，但難叫名、印在一般紙上弱。靛藍好叫名、印刷穩，但附近已經擠了五家同業，台灣的大亞也在裡面。對照 Romaniuk 的兩個條件：要讓很多人一看就想到你（名氣），也要只屬於你（獨特）。叫得出名字對前者有幫助，附近沒人用對後者有幫助（這段是推論）。</p>
<p class="learn"><b>兩者一樣的地方：</b>都夠深，配工程黃靠明暗差分得開；白字都清楚。</p>
<p class="learn"><b>要更正的一件事：</b>配色建議書第 5 頁寫「同行沒有人用深青」，不成立。台灣同業補充報告裡，華通衛生行的深青綠 #005959 跟深青只差 9.3。</p>
<p class="cap">色差是 CIEDE2000，用 colour-tool 算，同業色來自 10-13 台灣同業報告與 10-17 國外同業報告。決定權在梁特助。</p>
''')

# ================= 五、改掉的判斷 =================
page('''
<div class="part">五、改掉的判斷、缺口與來源</div>
<h3>這次改掉的判斷</h3>
<ol class="mid">
<li><b>以前</b>從色相環挑輔色、第三色。<b>現在</b>先定深淺差和比例，同業的兩色 logo 都靠明度拉開。</li>
<li><b>以前</b>以為工程黃能幫崧淳被認出來。<b>現在</b>知道橘黃是全行業共用的施工色，認出崧淳要靠主色。</li>
<li><b>以前</b>只看色碼、色差、對比。<b>現在</b>還要看叫不叫得出名字。</li>
<li><b>以前</b>在螢幕上判斷深色。<b>現在</b>要看印在一般紙上、遠看的樣子。</li>
<li><b>以前</b>說「同行沒有人用深青」。<b>現在</b>更正：華通衛生行差 9.3。</li>
<li><b>以前</b>覺得空位就是好。<b>現在</b>知道空位常有原因，要先查它為什麼空。</li>
<li><b>以前</b>拿名字做文字遊戲當配色理由。<b>現在</b>理由要是公司自己的目標或工作需要。</li>
<li><b>以前</b>交件用米色底、間隔號。<b>現在</b>改白底（美感串發現）。</li>
</ol>
<h3>還不知道的</h3>
<ul class="mid">
<li>色名、遠看都是模型，沒有找真人測。</li>
<li>印刷是用公開特性資料推估，要實體打樣才算數。</li>
<li>色名資料的中文受試者沒有分台灣、中國。</li>
<li>崧淳自己的工程資料（服務範圍、案例、員工）還沒有，所以「公司自己的事」還寫不出來。</li>
<li>雲端看不到設計網站，照片和手冊都是在你電腦上抓的。</li>
</ul>
''')

page('''
<h3>來源與可信度</h3>
<table class="t src"><tr><th>來源</th><th>拿到什麼</th><th>程度</th></tr>
<tr><td>48 家國外同業 logo 色、121 張官網實景照</td><td>分組、反光衣計數、取色</td><td>原始檔已看</td></tr>
<tr><td>Veolia《Essentials of the Graphic Charter》2024-03</td><td>第 3、5、7 頁</td><td>原文已讀</td></tr>
<tr><td>Heer 與 Stone 2012，c3 色名模型（GitHub）</td><td>英文色名分布</td><td>資料與程式已跑</td></tr>
<tr><td>Kim 等人 2019，uwdata 多語色名資料（GitHub）</td><td>中文色名分布</td><td>資料已跑</td></tr>
<tr><td>Zhang 與 Wandell 1996，S-CIELAB（ISETCam 程式）</td><td>遠看模擬</td><td>程式已讀並重寫</td></tr>
<tr><td>FOGRA39L、FOGRA47L 印刷特性資料（colord 收錄，CC0）</td><td>印刷推估</td><td>資料已跑</td></tr>
<tr><td>meodai/skill.color-expert（GitHub）</td><td>60-30-10、互補色算法、性格配色、論文整理</td><td>原文已讀</td></tr>
<tr><td>Schloss 與 Palmer 2011；Koenderink 等人 2026</td><td>兩色和諧、冷色分得粗</td><td>讀到整理稿，未讀原文</td></tr>
<tr><td>Palmer 與 Schloss 2010；Bae 等人 2015；CIE 208:2014</td><td>最不喜歡的顏色、記憶偏移、面積效應</td><td>只讀到摘要</td></tr>
<tr><td>Romaniuk（Ehrenberg-Bass）</td><td>好認、共用較弱、不要一直改</td><td>訪談與報導摘要</td></tr>
<tr><td>Ellen Divers；品牌定位影片</td><td>性格配色、定位</td><td>單一轉述，可信度低</td></tr>
<tr><td>美感串（PR #32）</td><td>3466 標誌量測、38 大師標誌、手冊頁</td><td>引用，未重做</td></tr>
<tr><td>Vattenfall、Caterpillar、Siemens、Rand、Bierut</td><td>設計理念</td><td>10-13、10-16 筆記</td></tr>
</table>
<p class="cap">論文原文網站（Springer、PMC 等）在雲端連不到，所以標「摘要」或「整理稿」的，都沒讀到原文。</p>
''')

page('''
<h3>這次找到的開源資源</h3>
<table class="t src"><tr><th>資源</th><th>用處</th><th>用了沒</th></tr>
<tr><td>meodai/skill.color-expert</td><td>目前找到最完整的色彩知識庫，181 份參考檔</td><td>讀了，沒安裝成 skill</td></tr>
<tr><td>connorgr/c3（Heer 與 Stone 色名模型）</td><td>算一個顏色好不好叫名</td><td>用了</td></tr>
<tr><td>uwdata 多語色名資料</td><td>中文色名</td><td>用了</td></tr>
<tr><td>ISETCam S-CIELAB</td><td>遠看模擬</td><td>用了，改寫成 Python</td></tr>
<tr><td>colord 收錄的 FOGRA 資料</td><td>印刷推估</td><td>用了</td></tr>
<tr><td>Anthropic frontend-design、rampstack logo-design</td><td>AI 樣子清單、標誌減法測試</td><td>美感串用了</td></tr>
<tr><td>ColorAide（Python 色彩套件）</td><td>交叉驗算</td><td>等你同意才安裝</td></tr>
</table>
<h3>檔案在哪</h3>
<p>這份 PDF、圖表數據和計算程式：專案資料夾「崧淳CI／研究／24_配色與設計理念學習_20261017」。文字筆記和程式也送到 gpt-collab 給 GPT。</p>
<p>報告裡的同業照片、大師標誌、手冊頁有版權，只放私人專案資料夾和你的電腦，不放進 gpt-collab。</p>
''')

# ---------- 組頁 ----------
CSS = open(R + 'report.css').read()
out = ['<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>配色與設計理念學習報告</title><style>', CSS, '</style></head><body>']
n = len(pages)
for i, (b, cls) in enumerate(pages, 1):
    foot = '' if 'nofoot' in cls else f'<div class="foot"><span>配色與設計理念學習報告</span><span>{i}</span></div>'
    out.append(f'<section class="page {cls}"><div class="inner">{b}</div>{foot}</section>')
out.append('</body></html>')
open(R + 'report.html', 'w').write('\n'.join(out))
print('pages', n)
