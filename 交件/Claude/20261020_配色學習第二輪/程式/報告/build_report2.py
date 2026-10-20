# 產生「配色與設計理念・第二輪」學習報告 HTML（A5 直式，固定頁）
import json, math, html
R = '/tmp/claude-0/report2/'
Q = '/tmp/claude-0/r2/'
tw = json.load(open(Q + 'tw/tw_peers.json'))
itt = json.load(open(Q + 'theory/itten_examples.json'))['examples']
sc = json.load(open(Q + 'scales/scales.json'))
ap = json.load(open(Q + 'models/data/apply.json'))
CSS = open(R + 'report.css').read() + open(R + 'extra.css').read()

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
def e(s): return html.escape(s)

pages = []
def page(body, part='', cls=''):
    pages.append((body, part, cls))

def fig(f, cap, h=None, cls='fg'):
    st = f' style="max-height:{h}mm"' if h else ''
    return f'<figure class="{cls}"><img src="img/{f}"{st}><figcaption>{cap}</figcaption></figure>'

def photo(f, cap, h=40):
    return f'<figure class="ph"><img src="img/{f}" style="height:{h}mm;max-height:none;object-fit:cover"><figcaption>{cap}</figcaption></figure>'

def chips_pair(cols, label='', note=''):
    top = ''.join(f'<div style="background:{c}"></div>' for c in cols)
    bot = ''.join(f'<div style="background:{grey_of(c)}"></div>' for c in cols)
    return (f'<div class="gp"><div class="gpt">{label}</div><div class="gpc">{top}</div>'
            f'<div class="gpc g">{bot}</div><div class="gpn">{note}</div></div>')

# ================= 封面 =================
page('''
<div class="cover">
  <h1 class="ct">配色與設計理念</h1>
  <p class="cs">第二輪：國內同業、色彩研究、配色模型、色階</p>
  <p class="cm">崧淳環保科技 CIS 學習報告<br>2026 年 10 月 20 日　Claude 整理，給梁特助</p>
  <figure class="cvph"><img src="img/v_dsd.jpg"><figcaption>香港渠務署的吸渠車。整台車漆成黃色，標誌只在車門上一小塊。照片：Negi，維基共享資源，CC BY-SA 3.0。</figcaption></figure>
  <p class="cn2">這是學習報告，不是配色提案。主色怎麼定，由梁特助決定；配色與設計由 GPT 主導，Claude 輔助。第一輪報告（10 月 17 日，33 頁）講過的不重講，只在被這輪更正時提到。</p>
</div>''', cls='nofoot')

# ================= 先講結論 =================
page('''
<h2>先講結論</h2>
<p class="lead">第一輪看的是國外 48 家。這一輪補上國內 21 家同業，讀了 4 篇色彩研究全文和 3 篇摘要，把 2 個有原始程式的配色模型、3 套設計系統的色階做法改寫來跑，也拿實際顏色去量 Itten、Munsell、PCCS 這些理論。學到八件事：</p>
<ol class="big">
<li><b>台灣同業跟國外一樣，一半只用一個顏色加黑白。</b>台灣 20 家有 10 家，國外 48 家有 23 家。</li>
<li><b>台灣用兩色的，幾乎都是藍或綠配紅、橘，而且兩色一樣深。</b>7 個多色 logo 有 6 個是對比色；兩色明度差中位 19.7，跟隨機配兩色（20.0）差不多，國外是 32.1。轉成黑白，兩色容易糊在一起。</li>
<li><b>台灣同業的主色沒有紅色。</b>17 家是藍 9、綠 6、橘 1、黃 1；國外 42 家有 11 家是紅。</li>
<li><b>同業的槽車也是黃橘色，跟自己 logo 的顏色無關。</b>宏隆、日技的槽車跟崧淳工程黃只差 4.3、6.7。黃車像反光衣一樣，是這一行共用的顏色（推論）。</li>
<li><b>人喜歡一個顏色，多半是喜歡那個顏色的東西。</b>柏克萊的研究：顏色好不好，80% 可以用「這個顏色的東西討不討喜」解釋。藍讓人想到晴空、淨水；褐讓人想到糞便、腐物。</li>
<li><b>兩色配，「喜歡」跟「和諧」不是同一件事。</b>色相相近，兩者都加分；深淺拉開，只會讓人更喜歡，不會更和諧。</li>
<li><b>教科書的配色規則，拿真實顏色去量，多半說不準。</b>Itten 七種對比互相重疊；和諧模板任兩色都放得進；和田三造的配色跟隨機配比，看不出明確規則。</li>
<li><b>設計系統不只給一個色號，而是把一個顏色展開成一排「各有工作」的深淺。</b>Radix 分 12 階、Material 分 13 個明度、Leonardo 照對比值去找色。</li>
</ol>''', '先講結論')

# ================= 這輪多了什麼、更正什麼 =================
page('''
<h2>這輪多了什麼，更正了上輪什麼</h2>
<table class="t">
<tr><th style="width:26mm">主題</th><th>第一輪</th><th>第二輪</th></tr>
<tr><td>國內同業</td><td>抄 10-11 的筆記，17 筆主色</td><td>21 家 31 個版本逐張量色、分組，跟國外用同一支程式比</td></tr>
<tr><td>色彩研究</td><td>只讀到整理稿</td><td>4 篇原文附頁碼，3 篇付費牆只讀摘要</td></tr>
<tr><td>配色模型</td><td>無</td><td>冷暖公式、兩色偏好分數、色名分散度，用原作者測試值驗過</td></tr>
<tr><td>配色理論</td><td>色相環、60-30-10 簡述</td><td>Itten、Albers、Munsell、PCCS、NCS、和田三造、Matsuda 逐一實算</td></tr>
<tr><td>色階</td><td>無</td><td>Radix、Material、Leonardo 改寫成程式，逐碼核對</td></tr>
<tr><td>資源與 skill</td><td>色彩知識庫一套</td><td>23 項，讀原始碼，量它們自己的說法</td></tr>
</table>
<h3>更正第一輪</h3>
<ol class="mid">
<li><b>國外 48 家的分組改成 23／8／1／9／1／6</b>（一個彩色／同色系／相鄰／對比／四色以上／只有黑白灰）。上輪寫 23／7／3／8／1／6。差在兩家：Sydney Water 兩色色相差 44.2°，剛好算同色系；Uisce Éireann 三色最大差 105°，算對比。「一個顏色加黑白最多」不變。</li>
<li><b>上輪的台灣 17 筆主色有 3 筆錯。</b>邦盛的紅是標語「專人為您服務」，不是公司名；綠邑 #254529、銘源 #082066 是網站顏色，不是 logo 色。</li>
<li><b>上輪說「最多人叫的色系中位 88%」用中文色名模型；這輪用英文色名模型重算，深青一樣最難叫名</b>，結論不變，見第 17 頁。</li>
</ol>
<div class="learn">怎麼看每條的可信度：<b>原文</b>＝打開原始檔讀到；<b>實算</b>＝我跑程式算的；<b>摘要</b>＝只讀到摘要或別人轉述；<b>目視</b>＝看圖判斷；<b>推論</b>＝我的推測。台灣同業、配色理論、配色模型、色階四部分的數字，都另外交給查核者獨立重算或回原始檔核對，錯的已改；論文引句附頁碼。</div>
''', '先講結論')

# ================= 第一部分：台灣同業 =================
page(f'''
<div class="part">一、國內同業</div>
<h2>21 家台灣同業的 logo</h2>
<p>來源有兩份：你電腦上的 14 家資料夾，和 10 月 13 日兩份台灣同業報告（登記 25 家，14 家查不到 logo）。兩邊重疊 3 家，共 21 家、31 個版本。</p>
{fig('fig_tw_logo_grid.png', '21 家的主版本，白底等比縮放。積德是智財局 2001 年的商標圖樣；九升、派浦崴洱、龍祥取自第三方網頁；邦盛、康立取網站橫幅上的字；順捷是墨色商標，不計色。圖為各公司所有，只供內部學習。', 128)}
''', '一、國內同業')

# 每家色條
rows = []
for p in tw:
    segs = []
    for c in (p.get('cols') or []):
        if c.get('share'): segs.append((c['hex'], c['share']))
    for nn in (p.get('neutral') or []):
        if nn.get('share') and nn['hex'].upper() != '#FFFFFF': segs.append((nn['hex'], nn['share']))
    tot = sum(s for _, s in segs) or 1
    bar = ''.join(f'<div style="background:{h};width:{100 * s / tot:.2f}%" title="{h}"></div>' for h, s in segs if s > 0)
    lab = []
    for h, s in segs:
        if s / tot >= 0.12: lab.append(f'{h} {round(100 * s / tot)}%')
    scheme = p.get('scheme') or '—'
    if not segs:
        bar = '<div style="background:#fff;width:100%"></div>'
        scheme = '只有白色反白版，不計色' if p.get('white_only') else '墨色商標，不計色'
    grad = '・漸層' if p.get('gradient') else ''
    rows.append(f'<div class="sr"><div class="sn">{e(p["company"])}</div><div class="sb">{bar}</div><div class="ss">{e(scheme)}{grad}</div></div>')
page(f'''
<h2>每家用了哪些顏色、各佔多少</h2>
<p class="sub">一條就是一個 logo，長度＝100%，每段寬度＝那個顏色佔 logo 非白部分的比例（白色不算）。右邊是配色方式。量法：只有幾個純色的圖逐點數，其他圖先去掉邊緣的雜色。（實算）</p>
<div class="stripes">{''.join(rows)}</div>
<p class="cap">多數台灣 logo 整個都是彩色（彩色佔非白部分的中位數 99.7%）；低於三成的只有源昌（橘只佔 4.5%，主體是深灰）。</p>
''', '一、國內同業')

page(f'''
<h2>配色方式：跟國外幾乎一樣</h2>
{fig('fig_scheme_compare.png', '台灣 20 家（扣掉墨色商標的順捷）對國外 48 家，同一支分組程式：OKLCH 色相差 45° 以內算同色系、45–90° 相鄰、90° 以上對比。（實算）', 78)}
<ul class="mid">
<li><b>一個彩色加黑白：</b>台灣 10／20（50%），國外 23／48（48%）。統計上沒有差別。</li>
<li><b>不一樣的是用兩色以上的：</b>台灣 7 家有 6 家是對比色、沒有同色系；國外 19 家是對比 9、同色系 8。台灣樣本小，差別還不能確定（p＝0.18）。</li>
<li><b>只看各家官網上的 logo 檔</b>（14 家）：7／0／0／5／1／1，方向一樣。</li>
</ul>
''', '一、國內同業')

# 多色 logo 轉黑白
multi = [p for p in tw if (p.get('n_chromatic') or 0) >= 2]
gps = []
for p in multi:
    cols = [c['hex'] for c in p['cols']]
    sh = '、'.join(f"{round(100 * c['share'])}%" for c in p['cols'])
    gps.append(chips_pair(cols, e(p['company']), f'ΔL* {p.get("dL", "")}<br>{sh}'))
page(f'''
<h2>用兩色的：對比色，但一樣深</h2>
<p>上排是 logo 裡的彩色，下排是同一個顏色轉成黑白。台灣多色 logo 的兩色，黑白下多半分不太開。</p>
<div class="gps">{''.join(gps)}</div>
<p class="cap">ΔL*＝最亮減最暗的彩色明度差；百分比＝各彩色佔非白部分的比例。天福有四個彩色。</p>
{fig('fig_dL.png', '多色 logo 的明度差：台灣 7 家中位 19.7，國外 19 家中位 32.1；紅虛線是隨機配兩個彩色的中位 20.0。國外比台灣多 12.4，但台灣只有 7 家，統計上還不能確定（p＝0.14）。（實算）', 40)}
<ul class="mid">
<li>6 家兩色 logo 裡，5 家是藍或綠配紅、橘。第二色真的只是一小點（不到一成）的只有大亞、日技、升野；華通的紅褐佔 28%、積德的紅 21–27%、宏隆的橘約一半。</li>
</ul>
''', '一、國內同業')

page(f'''
<h2>主色：藍綠為主，沒有紅</h2>
{fig('fig_hue_ring.png', '每家主色在色相環上的位置：左國外 42 家、右台灣 17 家（有彩色主色的才列）。（實算）', 66)}
<table class="t">
<tr><th>主色</th><th>台灣 17 家</th><th>國外 42 家</th></tr>
<tr><td>藍</td><td>9</td><td>21</td></tr>
<tr><td>綠</td><td>6</td><td>5</td></tr>
<tr><td>紅</td><td>0</td><td>11</td></tr>
<tr><td>橘、黃</td><td>2（源昌、升野）</td><td>2</td></tr>
<tr><td>青、紫</td><td>0</td><td>3</td></tr>
</table>
<p class="cap">「台灣沒有紅主色」單獨看算顯著（p＝0.024），但這輪做了約 8 個比較、沒有做多重比較校正，只能當方向看。台灣主色明度中位 0.536、國外 0.564；彩度 0.129 對 0.149，台灣略暗、略灰。</p>
''', '一、國內同業')

page('''
<h2>漸層、毛筆字、畫什麼</h2>
<table class="t">
<tr><th style="width:28mm">項目</th><th>台灣</th><th>對照</th></tr>
<tr><td>用漸層</td><td>6／20（大亞、久大、宏隆、康立、積德、龍祥）；只算官網 logo 檔 3／14</td><td>國外上輪文字記到至少 4／48（只是下限）</td></tr>
<tr><td>字（目視）</td><td>黑體 11、毛筆 4（源昌、宏隆、康立、一元）、只有圖沒有字 4、明體或楷體 2（逸居公司名是明體）</td><td>升野的粗筆帶毛筆感，算黑體有爭議；改算毛筆就是黑體 10、毛筆 5</td></tr>
<tr><td>圖形（目視，可多項）</td><td>只有字 6、水滴水波 5、箭頭循環 4、管 3、字母 3、抽象 2</td><td>10-11 筆記的「水滴、管件、葉片」大致成立</td></tr>
<tr><td>畫出本業的</td><td>只有升野的圖形畫了管內攝影車</td><td>其他家看圖猜不出是清管或攝影</td></tr>
</table>
<div class="learn">讀法（推論）：台灣小同業比較常用漸層、毛筆字，跟國外大公司的平面單色 logo 不同。第一輪學到「縮小、印刷、刺繡時漸層和細筆最先壞掉」，所以這不是差異化的機會，而是同業留下的坑。</div>
<p class="cap">漸層判斷靠目視加量測明度跨度（例：久大藍 0.25、龍祥綠 0.33）。九升小圖看不清。字形分類沒有字型檔可對。</p>
''', '一、國內同業')

page(f'''
<h2>車身：同業的槽車也是黃橘色</h2>
<div class="two">
{photo('tw_honglong.jpg', '宏隆：黃色槽體。logo 主色是綠。', 30)}
{photo('tw_tianfu.jpg', '天福：白色槽車。logo 主色是藍。', 30)}
{photo('tw_yiyuan.jpg', '一元：淡黃車身。logo 主色是藍。', 30)}
{photo('tw_huatong.jpg', '華通：綠色槽體，跟 logo 同色相。', 30)}
</div>
{fig('fig_vehicle_colours.png', '從照片裁切量的車身色，對照各家 logo 色與崧淳工程黃 #D68702。照片受光線影響，只是近似。日技的車照解析度太低沒放，只用來量色。（實算）', 34)}
<ul class="mid">
<li>宏隆、日技、派浦崴洱、一元的槽車是黃橘，跟工程黃差 4.3、6.7、13.9、14.8，跟各自 logo 色無關。</li>
<li>把 logo 色直接漆成整台車的，只看到華通（綠槽）。天福是白槽車、大亞與逸居是藍車頭（可能是原廠車色）。</li>
</ul>
<p class="cap">照片取自各公司網站與同業報告，只供內部學習。</p>
''', '一、國內同業')

page(f'''
<h2>深青、靛藍離台灣同業多遠</h2>
<p class="sub">只列事實，不做取捨。色差用 CIEDE2000，小於 10 算「看得出很像」，第一輪用的是同一條線。</p>
{fig('fig_candidates_dE.png', '兩個主色候選跟最近三家台灣主色的色差。大亞 #243952 是槽體漸層的深端，大亞 logo 面積最大的是黑（41–45%）。（實算）', 66)}
<table class="t">
<tr><th></th><th>深青 #0C424A</th><th>靛藍 #333D66</th></tr>
<tr><td>最近的台灣主色</td><td>大亞 14.0、一元 20.2、積德 21.9</td><td>大亞 7.0、一元 10.1、天福 18.2</td></tr>
<tr><td>10 以內的台灣主色</td><td>0 家</td><td>1 家（大亞）</td></tr>
<tr><td>算進次色與其他版本</td><td>華通衛生行的青 #005959（9.3）</td><td>—</td></tr>
<tr><td>第一輪：國外最近</td><td>Ventia 16.7</td><td>Insituform 6.7（10 以內 5 家）</td></tr>
</table>
''', '一、國內同業')

# ================= 第二部分：色彩研究 =================
page('''
<div class="part">二、色彩研究：人怎麼感受顏色</div>
<h2>喜歡一個顏色，是喜歡那個顏色的東西</h2>
<p class="sub">Palmer &amp; Schloss 2010，美國國家科學院院刊（PNAS）。原文已讀。</p>
<div class="chips">
<div class="chip" style="width:24mm"><div class="sw" style="background:#3E7CC1;height:12mm"></div><div class="cn">藍、青：晴空、淨水</div><div class="ch">最受喜愛</div></div>
<div class="chip" style="width:24mm"><div class="sw" style="background:#7A5A2E;height:12mm"></div><div class="cn">褐：糞便、腐物</div><div class="ch">不受喜愛</div></div>
<div class="chip" style="width:24mm"><div class="sw" style="background:#8E8A2A;height:12mm"></div><div class="cn">暗黃、黃綠</div><div class="ch">偏好曲線最低處</div></div>
</div>
<p class="cap" style="margin-top:-1mm">色塊是我畫的示意，不是論文的色票。</p>
<ul class="mid">
<li>48 位受試者看 32 個顏色打分數。另一批人寫出每個顏色會想到的東西，再評那些東西討不討喜。</li>
<li>「這個顏色的東西平均討不討喜」跟「這個顏色受不受喜愛」相關 0.893，<b>單一個變項就解釋 80%</b>（原文 p.8879）。比錐細胞模型（37%）、色貌模型（60%）、Ou 的色彩情感模型（55%）都高。</li>
<li>它抓到曲線的形狀：藍最高、黃綠最低、鮮的比濁的好、暗黃附近最低。失準兩處：深橘（偏褐）實際更不受喜愛，作者推測是巧克力、咖啡拉高了預測（p.8879）。</li>
<li>這篇被 Google 的 Material 配色程式引用：它把「暗黃綠」寫成要自動提亮的不喜歡色（程式註解，原文已讀）。</li>
</ul>
<div class="learn">對清淤業的意思（推論）：這行每天碰的正是糞便、汙泥、腐物。顏色會讓人想到什麼東西，比色票本身的好壞更重要。工程黃在 Material 的不喜歡區外（色相差 20.7°），但這是螢幕上的小色塊實驗，不是車身。</div>
''', '二、色彩研究')

page('''
<h2>兩色配：「喜歡」跟「和諧」不一樣</h2>
<p class="sub">Schloss &amp; Palmer 2011，Attention, Perception &amp; Psychophysics。原文已讀。</p>
<ul class="mid">
<li>同一批 48 人，32 個顏色組成 992 組「小方塊放在大方塊上」，分別評喜不喜歡、和不和諧（p.554）。</li>
<li><b>色相相近：</b>喜歡和和諧都加分（p.551）。</li>
<li><b>深淺拉開：</b>只讓人更喜歡，不會更覺得和諧。把和諧與兩色各自的喜好放進模型後，明度差還能多解釋 4.5%（p.560）。</li>
<li><b>和諧靠什麼：</b>色相近、偏冷、不太鮮、冷暖程度接近，共解釋 67.3%（p.560）。</li>
<li>平均來看，喜歡跟和諧相關 0.79；但每個人差很多，從 −0.03 到 0.75（p.559、561）。</li>
<li><b>前景色那一題方向相反：</b>色相差越大，前景色越受喜愛，但限於兩色明度相近時（p.567）。淺色放在深底、深色放在淺底，比較受喜愛（p.566）。</li>
</ul>
<h3>Ou &amp; Luo 2006 的和諧模型（摘要）</h3>
<p>由彩度差、明度和、明度差、色相四項組成；色相越近越和諧，跟 Schloss 的結果一致（兩份來源）。「明度差小於約 15 會降低和諧」「藍最容易和諧、紅最不容易」只見於一份專利，佐證不足。公式拿不到原文，這輪不用。</p>
<div class="learn">跟第一輪「明度拉開」連起來（推論）：國外同業多色 logo 拉開深淺，符合「讓人更喜歡」；但和諧另外靠色相相近。兩件事要分開談。</div>
''', '二、色彩研究')

page('''
<h2>顏色的情緒：30 國很像</h2>
<p class="sub">Jonauskaite 等 2020，Psychological Science。作者接受稿已讀。</p>
<ul class="mid">
<li>30 國、4,598 人、22 種母語，把 20 種情緒配給 12 個顏色名稱（p.6）。<b>給的是顏色名稱，不是色塊</b>（p.13）。</li>
<li>各國跟全球平均的相似度 0.88（埃及 0.684 到西班牙 0.941）；國與國之間平均 0.78（p.21）。</li>
<li>每一國都一樣：紅與黑的情緒聯想最多，<b>褐最少</b>（p.23）。</li>
<li>最明顯的聯想：黃—喜悅；橙—喜悅、好玩；白—安心；灰—悲傷、失望。藍沒有進入最明顯的清單（p.19–20）。</li>
</ul>
<h3>顏色記憶會往「名字的中心」偏</h3>
<p class="sub">Bae 等 2015，Journal of Experimental Psychology: General。原文已讀。</p>
<p>人記住的顏色，會被拉離兩個色名的交界、往最典型的那個顏色靠；直接看著配也有同樣偏差（摘要 p.2）。受試者只有 3 到 10 人，是知覺實驗。</p>
<div class="learn">跟色名連起來（推論）：深青剛好落在「綠」和「藍」的交界，第一輪中文模型兩邊各 38%。這篇的結果暗示，人回想時可能把它記成偏綠或偏藍，而不是原本的深青。這是推論，沒有實驗測過深青。</div>
<h3>只讀到摘要、不拿來下結論的</h3>
<ul class="mid">
<li>Ou 等 2004：單色有三個情感因子，活動、重量、冷暖（三份來源一致）。</li>
<li>Labrecque &amp; Milne 2012「紅＝興奮、藍＝能幹」：只見於標題和非學術網站，佐證不足。</li>
<li>網路流傳的「藍色讓 74% 的人覺得可信」查不到出處，不要用。</li>
</ul>
''', '二、色彩研究')

# ================= 第三部分：模型 =================
page(f'''
<div class="part">三、能算的配色模型</div>
<h2>冷暖公式：深青、靛藍分不出來</h2>
<p class="sub">Ou 的冷暖公式。原論文付費牆；Google Material Color Utilities 的程式裡有完整公式和測試值，註明出自 Ou、Woodcock、Wright（原文已讀，程式沒寫年份），我改寫後全部對上。</p>
{fig('fig_single_wc_L_v2.png', '橫軸：冷暖（大於 0 偏暖）；縱軸：明度 L*。42 家國外同業主色與崧淳三色。（實算）', 78)}
<ul class="mid">
<li>國外同業主色 28 冷、14 暖，中位 −0.93。深青 −0.90、靛藍 −0.85，在 42 家的中位附近；但 28 家偏冷的同業裡有 21 家比它們更冷，所以屬冷群裡較不冷的一側。工程黃 +1.30。</li>
<li>同業在圖上分成「藍綠」和「紅橘」兩群，中間幾乎沒有人（目視）。</li>
<li>這個公式只看色相和鮮度，深青和靛藍色相差 70°，冷暖分數卻幾乎一樣。</li>
</ul>
''', '三、配色模型')

page(f'''
<h2>兩色偏好分數：同業比隨機高</h2>
<p class="sub">Colorgorical（Gramazio、Laidlaw、Schloss 2017）把上一頁 Schloss &amp; Palmer 2011 的實驗寫成公式：明度差加分、色相差扣分、兩色越冷越加分。原始碼已讀，作者的色差上下限重現了。</p>
{fig('fig_pair_dL_pp_v2.png', '橫軸：兩色明度差；縱軸：兩色偏好分數。灰點是隨機兩色，小雙色圓是國外同業 logo 的實際兩色，黑框是本報告比較的配對。（實算）', 74)}
<table class="t">
<tr><th>兩色偏好分數中位</th><th>總分</th><th>明度項</th><th>冷度項</th></tr>
<tr><td>同業 logo 實際配對（30 對）</td><td>47.6</td><td>20.7</td><td>52.2</td></tr>
<tr><td>同業顏色打亂重配（2,115 對）</td><td>26.4</td><td>11.3</td><td>42.5</td></tr>
<tr><td>隨機兩色（5,000 對）</td><td>15.7</td><td>15.0</td><td>26.5</td></tr>
</table>
<p class="cap">跟打亂重配比，冷度項和明度項各多約 9.5，兩者差不多。這個差距也不穩：從打亂的配對裡隨機抽 30 對，約 5% 的機會中位數也到 47.6；只在 19 家多色公司之間打亂，中位數是 40.4。這個分數只是柏克萊 48 人看螢幕上小方塊配大方塊的平均喜好，<b>不等於好看</b>，也不知道放大到車身、招牌還準不準。</p>
''', '三、配色模型')

def namebar(name, hexv, terms, note):
    segs = ''.join(f'<div style="width:{t[1]*100:.1f}%;background:{c};color:#fff">{e(t[0])} {round(t[1]*100)}%</div>' for t, c in zip(terms, ['#2F2F2F', '#555555', '#767676']))
    return (f'<div class="nr"><div class="nsw" style="background:{hexv}"></div><div class="nb"><div class="nn">{name} <span>{hexv}</span></div>'
            f'<div class="bar">{segs}</div><div class="nt">{note}</div></div></div>')
T = ap['targets_single']
# 查核：靛藍 blue 是 49/228＝21.5%，原檔先進位成 0.215 再進位成 22%
T['靛藍']['cg_top_terms'] = [['navyblue', 0.237], ['blue', 49 / 228], ['darkblue', 0.184]]
page(f'''
<h2>叫不叫得出名字：換一個模型，結果一樣</h2>
<p>第一輪用中文色名資料算出「深青最難叫名」。這輪用 Colorgorical 內建的英文色名資料（xkcd，153 個名字）再算一次：</p>
{namebar('深青', T['深青']['hex'], T['深青']['cg_top_terms'], '名字分散度 0.935，42 個國外同業主色裡最高（同業中位 0.483）。前三名各約一成二，沒有一個名字站得住。')}
{namebar('靛藍', T['靛藍']['hex'], T['靛藍']['cg_top_terms'], '分散度 0.746（同業第 95 百分位）。細分名字很散，但都是「藍」家族；第一輪中文模型 68% 叫藍。')}
{namebar('工程黃', T['工程黃']['hex'], T['工程黃']['cg_top_terms'], '英文裡最常被叫 orange（57%），不是 yellow。')}
<ul class="mid">
<li>同業 logo 實際的兩色，色名差中位 0.85，比隨機（0.985）低：同業常把同一色名家族的深淺放在一起。（實算）</li>
<li>深青×工程黃、靛藍×工程黃的色名差都是 1.00，英文叫法完全不重疊。</li>
</ul>
<div class="learn">兩個資料、兩種語言都指向同一件事：深青不好叫名，靛藍好叫但歸在大家都在用的「藍」。哪一個比較好，要看要的是「好記」還是「不撞色」，由梁特助判斷。</div>
''', '三、配色模型')

page('''
<h2>模型會錯在哪裡</h2>
<ol class="mid">
<li><b>程式跟論文不一致。</b>Colorgorical 算色相差沒有繞回 360°，跨過紅色的配對會被多扣分。隨機兩色有 27% 受影響，國外同業 30 對裡 5 對受影響。靛藍×工程黃照程式算 −2.6，照原意算 14.2。（原文＋實算）</li>
<li><b>正規化上下限重現不了。</b>色差的上下限用 8,325 色全配對重現了，兩色偏好的上下限試了 5 種算法都對不上，所以只比排名，不比絕對分數。</li>
<li><b>兩套規則對同一個顏色意見不同。</b>Colorgorical 作者手訂「黃褐懲罰區」（Lab 色相 70–115、明度 75 以下，分數乘 0.8），工程黃在裡面；國外同業 66 個彩色只有 Mini-Cam 的黃在裡面。Material 的不喜歡區（暗黃綠）則不包含工程黃，差 20.7°。</li>
<li><b>受試者與情境很窄。</b>Colorgorical 的偏好資料是柏克萊 48 人看螢幕色塊、灰背景；Ou 的冷暖也是實驗室色塊。沒有台灣人、沒有車身、沒有日光。</li>
</ol>
<div class="learn">學到的（推論）：模型分數是「一群人在實驗室的平均反應」，能幫忙找出明顯的問題（例如兩色太近、轉黑白糊掉），不能用來決定哪個顏色比較好看。程式裡的錯也要自己驗過才知道。</div>
<p class="cap">Ou 的另外兩個因子（輕重、主動被動）和 Ou &amp; Luo 2006 的和諧公式沒拿到原文，沒有算。Palettailor 只算分辨度、色名差和兩兩最小色差，沒有偏好或和諧分數。</p>
''', '三、配色模型')

# ================= 第四部分：理論 =================
def itten_row(title, sub, cols, note, flag=False):
    top = ''.join(f'<div style="background:{c}"></div>' for c in cols)
    bot = ''.join(f'<div style="background:{grey_of(c)}"></div>' for c in cols)
    cls = ' fl' if flag else ''
    return (f'<div class="ir{cls}"><div class="it"><b>{title}</b><br><span>{sub}</span><br><span>{note}</span></div>'
            f'<div class="ic"><div class="icc">{top}</div><div class="icc g">{bot}</div></div></div>')
I = itt
ir = [itten_row('色相對比', 'Watercare 四色', I['色相對比'][0]['cols'], '三群色相'),
      itten_row('明暗對比', 'Insituform 同色相', [I['明暗對比'][1]['a']['hex'], I['明暗對比'][1]['b']['hex']], f"明度差 {I['明暗對比'][1]['dL']}"),
      itten_row('冷暖對比', 'Watercare 紅＋藍', [I['冷暖對比'][0]['a']['hex'], I['冷暖對比'][0]['b']['hex']], f"明度差只有 {I['冷暖對比'][0]['dL']}"),
      itten_row('補色對比', 'Kier 紅＋藍綠', [I['補色對比'][0]['a']['hex'], I['補色對比'][0]['b']['hex']], '色相差 179.5°，明度差 0.6'),
      itten_row('彩度對比', 'Tideway 青綠＋灰', [I['彩度對比'][0]['a']['hex'], I['彩度對比'][0]['b']['hex']], f"明度差 {I['彩度對比'][0]['dL']}"),
      itten_row('同時對比（示意）', 'Wessex 的灰放在 Kanal-Türpe 橘、CUES 藍上', [itt['同時對比']['bg1']['hex'], itt['同時對比']['gray']['hex'], itt['同時對比']['bg2']['hex']], '三家的顏色拼的，不是單一 logo', True)]
page(f'''
<div class="part">四、配色理論拿來量</div>
<h2>Itten 七種對比：用同業的真實顏色看</h2>
<p class="sub">上排是原色，下排轉成黑白。七種裡五種在單一同業 logo 裡找得到；面積對比沒有資料，同時對比只能拼示意。（實算）</p>
<div class="irs">{''.join(ir)}</div>
<ul class="mid">
<li><b>補色、冷暖這兩組轉黑白就糊掉</b>：Kier、Watercare 的紅配藍，兩色幾乎一樣亮。</li>
<li><b>學界的批評</b>（Hirschler 演講逐字稿，原文已讀）：色相、明暗其實是顏色的屬性，不是對比；冷暖是相對的；面積公式沒算鮮度；一對顏色就能同時展現七種，所以七種互相重疊。</li>
</ul>
''', '四、配色理論')

page(f'''
<h2>同一個黃，放在不同底上</h2>
<p class="sub">Albers《色彩互動》的核心：顏色看起來怎樣，看它旁邊是什麼。這是示意，不是配色提案。</p>
{fig('fig_simul_contrast.png', '同一個工程黃 #D68702 放在深青、靛藍、白、中灰、黑上。下方是亮度比、色差、明度差，和色貌模型 CIECAM02 預測「看起來多亮」（J）。黑底的背景亮度用自訂下限 1。（實算）', 54)}
<table class="t">
<tr><th>底色</th><th>深青</th><th>靛藍</th><th>白</th><th>中灰</th><th>黑</th></tr>
<tr><td>亮度比</td><td>3.87</td><td>3.66</td><td>2.87</td><td>1.56</td><td>7.33</td></tr>
<tr><td>看起來多亮 J</td><td>59.0</td><td>58.7</td><td>46.1</td><td>55.1</td><td>61.0</td></tr>
</table>
<ul class="mid">
<li>同一個黃，在黑底上看起來比在白底上亮很多（J 61 對 46）。</li>
<li>深青底和靛藍底，模型算「看起來多亮」只差 0.3；亮度比 3.87 對 3.66、色差 52.7 對 56.2。</li>
<li>色相會往底色的補色偏（深青底會讓黃偏紅橘、靛藍底偏黃），但這個模型不算色相偏移，偏多少算不出來。</li>
</ul>
''', '四、配色理論')

page(f'''
<h2>三個顏色在 Munsell、PCCS 的位置</h2>
{fig('fig_munsell_vc.png', 'Munsell 明度（縱）×彩度（橫）：42 家國外同業主色（圓點）與崧淳三色（方塊）。換算先用 colour-science 的測試表驗過，色相誤差中位 0.03 步。（實算）', 62)}
<table class="t">
<tr><th></th><th>深青</th><th>靛藍</th><th>工程黃</th><th>國外同業主色</th></tr>
<tr><td>Munsell</td><td>0.6B 2.5/3.7</td><td>7.0PB 2.7/5.7</td><td>7.7YR 6.2/11.7</td><td>彩度最低 4.9</td></tr>
<tr><td>PCCS 色調</td><td>dk 暗</td><td>dk 暗（靠近 d）</td><td>s 強</td><td>v 鮮 21、b 8、dk 只有 2</td></tr>
<tr><td>相對彩度</td><td>0.91</td><td>0.30</td><td>1.00</td><td>中位 0.99</td></tr>
<tr><td>ISCC-NBS 名稱</td><td>暗綠藍</td><td>中等紫藍</td><td>深橘黃</td><td></td></tr>
</table>
<ul class="mid">
<li><b>兩種量法結論相反。</b>Munsell 彩度看絕對值，深青 3.7 比 42 家同業主色都低。相對彩度看「同深淺、同色相，螢幕上最多能多鮮」，深青 0.91 已接近上限，靛藍 0.30 比所有同業主色都低，還有很多空間。</li>
<li>同業主色一半是 PCCS 的 v（鮮）；兩個候選都是 dk（暗），同業只有 2 家。</li>
</ul>
''', '四、配色理論')

page(f'''
<h2>教科書規則量起來</h2>
{fig('fig_wada.png', '和田三造《配色總鑑》123 組兩色配色，對照同一盒顏色隨機配（每次重抽，2 萬次×2）。（實算）', 50)}
<ul class="mid">
<li><b>和田三造的兩色配色：</b>明度差、同色調比例跟隨機配沒有測到差別；色相相近（30° 內）的比例 11.7% 對 17.7%，在顯著的邊界（p 約 0.09），方向是和田刻意避開同色相。123 組太少，只能說沒測到明顯差別。</li>
<li><b>Matsuda 和諧模板</b>（經 Cohen-Or 2006 的程式）：19 家多色 logo 有 18 家放得進；但隨機兩色 100% 放得進，對兩色 logo 沒有篩選力。</li>
<li><b>「泥濁色」規則</b>（pro-color-harmonies）：國外同業 66 個彩色有 21 個落在它說的泥濁區，崧淳三色都不在。規則把大量真實品牌色都判成不好。</li>
<li><b>NCS</b>：以白、黑、紅、黃、綠、藍六個基本色描述，沒有明度軸。「最暖是橘、最冷是藍綠」是 Briggs 的推測，不是 NCS 的規定。</li>
</ul>
<div class="learn">學到的（推論）：規則多半是「事後解釋好作品」，拿來挑顏色篩不出東西。真正量得出差別的，還是第一輪那幾件事：幾個顏色、深淺拉多開、叫不叫得出名字。</div>
''', '四、配色理論')

page('''
<h2>面積比例：公式彼此差 2 倍</h2>
<p>歌德給每個顏色一個「亮度權重」（紫 1/4、藍 1/3、綠 1/2、紅 1/2、橘 2/3），Itten 照這個說亮的顏色面積要小、暗的要大，例如黃比紫 1:3。（摘要）</p>
<ul class="mid">
<li>拿 Munsell 1943 年資料裡各色相最鮮那一點的明度去對：黃、橘、紅、藍對得上；紫、綠的最鮮點有兩個明度並列，取法不同，黃比紫是 1:3.0 或 1:2.25。接不接近歌德，看怎麼取。這些是理論極限點，不是實體色票。（實算）</li>
<li>兩條「平衡面積」公式套在工程黃上：配深青，「面積跟明度 L* 成反比」說黃佔 28.5%，Munsell 式說 11.3%，差 2.5 倍；配靛藍是 29.8% 對 17.2%，差 1.7 倍。（實算，示意）</li>
<li>沒有一條公式有實驗證明「面積平衡就好看」。</li>
</ul>
<div class="scl">兩條公式算出的黃色面積（示意，不是建議比例）</div>
<div class="arw"><span>配深青　L* 反比 28.5%</span><div class="arb"><div style="background:#0C424A;width:71.5%"></div><div style="background:#D68702;width:28.5%"></div></div></div>
<div class="arw"><span>配深青　Munsell 式 11.3%</span><div class="arb"><div style="background:#0C424A;width:88.7%"></div><div style="background:#D68702;width:11.3%"></div></div></div>
<div class="arw"><span>配靛藍　L* 反比 29.8%</span><div class="arb"><div style="background:#333D66;width:70.2%"></div><div style="background:#D68702;width:29.8%"></div></div></div>
<div class="arw"><span>配靛藍　Munsell 式 17.2%</span><div class="arb"><div style="background:#333D66;width:82.8%"></div><div style="background:#D68702;width:17.2%"></div></div></div>
<div class="learn">跟第一輪接起來：第一輪講 60-30-10 和 Veolia「同畫面最多兩色、logo 永遠紅」。真實手冊是規定「哪裡用、用多大」，不是算一個比例。面積公式可以當起點，不是答案。</div>
''', '四、配色理論')

# ================= 第五部分：色階 =================
mat = sc['material']['tonal_spot_palettes']['primary']['tones']
rad = sc['radix']['accent_scale']
mat_strip = ''.join(f'<div style="background:{t["hex"]};color:{ink(t["hex"])}">{t["tone"]}</div>' for t in mat)
rad_strip = ''.join(f'<div style="background:{t["hex"]};color:{ink(t["hex"])}">{t["step"]}</div>' for t in rad)
page(f'''
<div class="part">五、一個顏色怎麼展開成一套</div>
<h2>三種做法</h2>
<p class="sub">用跟崧淳無關的 Vattenfall 藍 #2071B5 示範。三套的原始碼都改寫成程式，用原庫的測試值逐碼核對過。（原文＋實算）</p>
{fig('fig_vattenfall_scales.png', '同一個藍用不同方法展開：Material 兩種變體、Radix 產生器與官方藍、Leonardo（照對比值）、Tailwind 藍。框線是原色的位置，只有 Radix 產生器那一列含原色。（實算）', 58)}
<ul class="mid">
<li><b>Material</b>：明度就是 tone，0 黑、100 白。預設變體會把主色鮮度固定在 36，不管原色多鮮；要保留原色鮮度得改用另一個變體。</li>
<li><b>Radix</b>：每一階有固定工作（下一頁）。品牌色放在第 9 階。</li>
<li><b>Leonardo</b>（Adobe）：先寫「這一階對白底要多少對比」，再沿著白—品牌色—黑那條線找到剛好的顏色。</li>
</ul>
''', '五、色階')

uses = ''.join(f'<tr><td><div class="tsw" style="background:{t["hex"]}"></div></td><td>{t["step"]}</td><td>{e(t["use"])}</td><td>{t["hex"]}</td><td>{t["wcag_vs_white"]}</td></tr>' for t in rad)
page(f'''
<h2>Radix 每一階做什麼</h2>
<table class="t tight">
<tr><th></th><th>階</th><th>用途（原文）</th><th>色碼</th><th>對白底</th></tr>
{uses}
</table>
<ul class="mid">
<li>Material 的角色也固定取某個 tone：淺色模式主按鈕 40、按鈕上的字 100、淺底容器 90、內文 10；深色模式主按鈕改 80。（原文）</li>
<li><b>驗算原文說法：</b>Radix 文件說第 11、12 階當字夠清楚（APCA 60、90 以上），31 個官方色系都成立。Material 文件說「tone 差 50 保證對比 4.5」，tone 50 對 100 實際只有 4.48。Radix 說「第 9 階最鮮」，23 個彩色色系只有 10 個成立。</li>
<li>Radix 產生器遇到偏深的品牌色會出問題：Vattenfall 藍（明度 46）展開後，第 11 階反而比第 10 階淺。</li>
</ul>
''', '五、色階')

C = sc['崧淳候選色_只列事實']['targets']
page(f'''
<h2>三個顏色放進色階裡</h2>
<p class="sub">只列事實。HCT 是 Material 用的色彩空間：色相、鮮度、明度。</p>
<table class="t">
<tr><th></th><th>深青</th><th>靛藍</th><th>工程黃</th></tr>
<tr><td>HCT</td><td>211／25／25</td><td>276／30／27</td><td>69／54／63</td></tr>
<tr><td>鮮度用到上限的幾成</td><td>93%</td><td>49%</td><td>99.7%</td></tr>
<tr><td>Radix 最近一階</td><td>cyan 12（3.5）</td><td>indigo 12（5.3）</td><td>amber 8（8.1）</td></tr>
<tr><td>那一階的工作</td><td>高對比文字</td><td>高對比文字</td><td>較強框線、焦點環</td></tr>
<tr><td>左：原色　右：那一階</td><td><div class="pr"><div style="background:#0C424A"></div><div style="background:#0d3c48"></div></div></td><td><div class="pr"><div style="background:#333D66"></div><div style="background:#1f2d5c"></div></div></td><td><div class="pr"><div style="background:#D68702"></div><div style="background:#e2a336"></div></div></td></tr>
</table>
<ul class="mid">
<li>國外同業 66 個 logo 色，最近的 Radix 階全落在第 7–12 階，中位色差 4.96；隨機 2,000 色中位 6.3。</li>
<li>深青、靛藍都比 Radix 的「實色」第 9 階深很多，最接近的是給字用的第 12 階。拿 Radix 產生器展開，它照樣把原色放在第 9 階，結果第 9 階比第 10、11 階還深（深青明度 25 對 33、47；靛藍 27 對 34、45），深淺順序倒過來。查核者另跑一個深藍也一樣。（實算）</li>
<li>工程黃已經在螢幕能顯示的最鮮邊上（99.7%），沒有更鮮的空間；深青也接近上限（93%）；靛藍還有一半的空間。</li>
</ul>
<div class="learn">學到的（推論）：主色不是一個色號就完了。真正上線時要有一整排深淺：淺底、框線、實色、文字。深的主色適合當字和實色，淺底要另外展開；這一步通常交給設計系統的方法，不靠手調。</div>
''', '五、色階')

# ================= 第六部分：美感串 =================
page('''
<div class="part">六、美感串交來的：造形、字體、版面</div>
<h2>標誌造形</h2>
<p class="sub">美感串第二輪整理，論文多半只讀到摘要；每條都跟出處逐條核對過。</p>
<ol class="mid">
<li><b>看得出賣什麼的標誌，對陌生品牌有利</b>，熟了好處變小；行業讓人聯想負面時反而扣分（Luffarelli 等 2019，摘要）。描述可以交給字標，不一定畫圖。</li>
<li><b>陌生品牌的圖形要跟名字一起出現</b>，圖加名字比只有一樣好看（Bresciani &amp; Del Ponte 2017，摘要）。同一篇：陌生標誌裡黑色比彩色吸引人。</li>
<li><b>外框：</b>購買風險高時讀成「保護」，低時讀成「拘束」（Fajardo 等 2016，摘要）。日、星、韓、港水務標誌都沒有外框。</li>
<li><b>有結構（對稱、規律、幾何）對講實用的品牌較有利</b>，講享樂的相反（Affonso &amp; Janiszewski 2023，摘要）。亞洲水務與經典企業 22 個標誌，多數只用一種手法；台電、中油的多元素徽章是例外，也是線最細的（寬的 1/290、1/140）。</li>
<li><b>圓讓人覺得舒適、尖角覺得耐用</b>，但旁邊文字講反就消失，也查不到重複驗證（Jiang 等 2016，摘要）。</li>
</ol>
<div class="learn">跟配色連起來（推論）：第 1 點的「行業負面聯想」跟第二部分 Palmer &amp; Schloss 的褐色、腐物是同一件事；清淤業的顏色和圖形都要避開讓人想到汙物的方向。</div>
''', '六、美感串')

page('''
<h2>中文字標與標準字</h2>
<ol class="mid">
<li><b>中文品牌名主要靠字形被記住</b>（Pan &amp; Schmitt 1996 等，摘要）。台灣受測者認為楷體最能代表台灣（黃耀明 2023，搜尋片段）；但 22 個亞洲標誌裡看得出中文字體的 7 個，沒有一個用楷體（6 個黑體或特製、1 個書法）。台灣同業 21 家：黑體 11、毛筆 4。</li>
<li><b>中文標準字要逐字調：</b>大小、重心、中宮、粗細靠眼睛；縮到 0.4 公分還要認得；英文另選，不用中文字型內建的（justfont、許瀚文、森澤，全文）。</li>
<li><b>反 AI 清單互相矛盾：</b>Anthropic 的 frontend-design 把米色底配襯線列為 AI 樣子，另一個開源 skill 卻把幾乎同色的暖白底配襯線當解方。報告版面用白底，不要把暖白當安全牌。（原文）</li>
</ol>
<h3>這輪沒做完</h3>
<ul class="mid">
<li>你電腦上的 4 篇日文字體論文、Jiang 2016 全文細節。</li>
<li>楷體、黑體縮小比較。</li>
</ul>
<p class="cap">這兩項要你在美感串回一句才會接著做。</p>
''', '六、美感串')

page(f'''
<h2>車身上的顏色與字</h2>
<div class="two">
{photo('v_tokyo.jpg', '東京都水道局：白車加一條藍帶，白字只在色帶裡。Ypy31，CC0。', 30)}
{photo('v_cpc.jpg', '台灣中油：白、紅、藍條紋。玄史生，CC0。', 30)}
{photo('v_taipower.jpg', '台電：整排黃色工程車。Solomon203，CC BY-SA 3.0。', 30)}
{photo('v_cht.jpg', '中華電信：黃車。Solomon203，CC BY-SA 3.0。', 30)}
</div>
<ul class="mid">
<li><b>整車漆色本身就是識別：</b>香港渠務署（封面）只在門上放標誌，靠整台黃車；台電、中華電信也是黃車。</li>
<li><b>色帶、條紋是這批 16 張車照最常見、最顯眼的手法</b>（東京都水道局、中油、中華電信）。淺色車一律深色字，白字只出現在色帶裡。</li>
<li><b>字要多大：</b>美國招牌研究約每 1 公分字高看 3.6 公尺，實際開車至少打 65 折。外照時黑字白底比白字黑底好認（Helvetica 29 對 26，USSC 表 1，全文）。</li>
</ul>
<div class="learn">跟國內同業連起來（推論）：黃色工程車在台灣已經被台電、中華電信、同業槽車共用。崧淳的黃車要被認出是崧淳，靠的不是黃，是車上的標誌、主色和字。</div>
''', '六、美感串')

# ================= 第七部分：資源 =================
page('''
<div class="part">七、開源資源與 skill</div>
<h2>這輪查到的 23 項</h2>
<table class="t src">
<tr><th>名稱</th><th>教什麼</th><th>有沒有用</th></tr>
<tr><td>Radix Colors＋網站文件（MIT）</td><td>12 階各有用途；品牌色另做自訂色階</td><td>有，最清楚的範例；產生器已改寫驗證</td></tr>
<tr><td>Material Color Utilities（Apache-2.0）</td><td>HCT、明度分階、角色對 tone；Ou 冷暖公式、不喜歡色規則</td><td>有，已改寫，測試值全對</td></tr>
<tr><td>Adobe Leonardo（Apache-2.0）</td><td>先定對比值再找色；自帶 Agent skill 與 MCP</td><td>有，已改寫；skill 未安裝</td></tr>
<tr><td>Colorgorical（Schloss 實驗室）</td><td>兩色偏好、色名差、色名分散度</td><td>有，但程式有錯（第 18 頁）</td></tr>
<tr><td>chroma.js（BSD／Apache）</td><td>RGB 內插中段會變暗，Lab 較好</td><td>有，驗算成立</td></tr>
<tr><td>culori、iWantHue、colorjs.io</td><td>色彩庫與多色並列配色</td><td>工具，對單一品牌色用處小</td></tr>
<tr><td>Tailwind 3.4.17 預設色</td><td>11 階、明度平均分布</td><td>對照組</td></tr>
<tr><td>UI Color Palette（Figma 外掛，MIT）</td><td>各系統刻度預設</td><td>對照表；Claude 外掛未安裝</td></tr>
<tr><td>anthropics/skills 三個</td><td>theme-factory、brand-guidelines、frontend-design</td><td>少；米色底出處在 frontend-design</td></tr>
<tr><td>knowledge-work-plugins 三個</td><td>design 檢查清單、品牌風格、資料視覺化</td><td>少；資料視覺化的「色弱友善」色盤量起來不成立</td></tr>
<tr><td>和田三造、ISCC-NBS 色名（npm）</td><td>日本配色總鑑、美國色名</td><td>有，已實算</td></tr>
<tr><td>colour-science、ColorHarmonization</td><td>Munsell 資料、Matsuda 模板</td><td>有，已實算</td></tr>
<tr><td>superdesign skill</td><td>前端設計</td><td>沒有</td></tr>
<tr><td>brand-studio、brand-md、Codesign、design-superpowers</td><td>外掛目錄找到</td><td>未安裝，原始碼找不到</td></tr>
</table>
<p class="cap">完整 23 項（網址、提交、授權）見文字版 resources.json。外掛目錄裡的「Design（Anthropic）」推定就是 knowledge-work-plugins 的 design 外掛。</p>
''', '七、資源')

page('''
<h2>skill 和工具也會錯</h2>
<ol class="mid">
<li><b>標「色弱友善」的色盤不一定友善。</b>knowledge-work-plugins 資料視覺化 skill 的 6 色，在紅色盲模擬下最小色差只有 2.02，比 92% 的隨機 6 色組還差。（實算）</li>
<li><b>官方文件的保證也要算。</b>Material「tone 差 50 保證 4.5」差一點不成立（4.48）；Radix「第 9 階最鮮」23 色系只有 10 個成立。</li>
<li><b>研究程式跟論文不一致。</b>Colorgorical 色相差沒繞回 360°。</li>
<li><b>Anthropic 自己的品牌色當字不夠清楚。</b>brand-guidelines 的橘、藍放在淺底上對比 2.96、2.78，所以它只用在非文字的形狀上。</li>
<li><b>反 AI 清單會過期、會互相矛盾</b>（上一部分第 3 點）。</li>
</ol>
<div class="learn">學到的：工具和 skill 是別人的判斷，不是規則。用之前先拿一兩個已知的顏色驗它，這輪 23 項裡有 5 項驗出問題。</div>
<h3>我想學但這個環境拿不到的</h3>
<ul class="mid">
<li>PCCS 色調配色原文、Moon–Spencer、Matsuda 原著、Itten 與 Albers 原書。</li>
<li>Ou 2004、Ou &amp; Luo 2006、Labrecque &amp; Milne 2012 全文（付費牆）。</li>
<li>台灣同業的 CIS 手冊或官方色號：沒有任何一家公開。</li>
</ul>
''', '七、資源')

# ================= 候選色事實表 =================
page('''
<div class="part">附：三個顏色這輪量到的事實</div>
<h2>深青、靛藍、工程黃</h2>
<p class="sub">把散在各頁的數字放在一起。只列事實，不做取捨；主色由梁特助決定。</p>
<table class="t ft">
<tr><th></th><th><span class="tsw" style="background:#0C424A"></span>深青</th><th><span class="tsw" style="background:#333D66"></span>靛藍</th><th><span class="tsw" style="background:#D68702"></span>工程黃</th></tr>
<tr><td>Munsell</td><td>0.6B 2.5/3.7</td><td>7.0PB 2.7/5.7</td><td>7.7YR 6.2/11.7</td></tr>
<tr><td>PCCS 色調</td><td>dk</td><td>dk（靠近 d）</td><td>s</td></tr>
<tr><td>相對彩度</td><td>0.91</td><td>0.30</td><td>1.00</td></tr>
<tr><td>冷暖（Ou）</td><td>−0.90</td><td>−0.85</td><td>+1.30</td></tr>
<tr><td>英文名分散度</td><td>0.935（同業最高）</td><td>0.746</td><td>0.592</td></tr>
<tr><td>中文色名（第一輪）</td><td>綠 38／藍 38</td><td>藍 68</td><td>—</td></tr>
<tr><td>Radix 最近一階</td><td>cyan 12</td><td>indigo 12</td><td>amber 8</td></tr>
<tr><td>配工程黃：亮度比</td><td>3.87</td><td>3.66</td><td></td></tr>
<tr><td>配工程黃：色差</td><td>52.7</td><td>56.2</td><td></td></tr>
<tr><td>配工程黃：兩色偏好</td><td>27.4</td><td>−2.6（照原意 14.2）</td><td></td></tr>
<tr><td>配白：兩色偏好</td><td>56.2</td><td>29.3</td><td></td></tr>
<tr><td>最近台灣主色</td><td>大亞 14.0</td><td>大亞 7.0</td><td></td></tr>
<tr><td>最近國外（第一輪）</td><td>Ventia 16.7</td><td>Insituform 6.7</td><td></td></tr>
</table>
<p class="cap">兩色偏好分數是模型對螢幕小色塊的平均喜好預測，不等於好看；配白的分數來自 Colorgorical 的內插表，原實驗沒有白色。色差小於 10 算很像。</p>
''', '附')

# ================= 沒做到 + 來源 =================
page('''
<h2>這輪的限制</h2>
<ul class="mid">
<li><b>台灣樣本小。</b>可算色 20 家、多色 7 家；約 8 個比較沒有做多重比較校正，p 值只當參考。</li>
<li><b>色碼都是螢幕圖檔量的。</b>沒有任何台灣同業公開 CIS 手冊或官方色號；JPEG 有色偏，積德掃描尤其大。車身色受光線影響。</li>
<li><b>版本不一定是現行的。</b>積德是 2001 年的商標圖樣，九升、派浦崴洱、龍祥是第三方網頁，邦盛、康立是網站橫幅。</li>
<li><b>論文 3 篇只有摘要。</b>Ou 的公式只拿到冷暖一條（從 Google 的程式裡）。</li>
<li><b>模型都是外國大學生看螢幕色塊。</b>沒有台灣人、沒有車身、沒有戶外光。</li>
<li><b>沒有真人看過。</b>所有結論都是資料和模型，沒有找人實際看崧淳的顏色。</li>
<li><b>美感串兩項未完成</b>（日文字體論文、楷體黑體縮小比較）。</li>
</ul>
<div class="learn">這份報告的數字、程式、資料都在專案資料夾 崧淳CI/研究/25_配色學習第二輪_20261019/，文字版同步到 gpt-collab 給 GPT。報告裡的第三方 logo 與照片只供內部學習，不放進公開的 repo。</div>
''', '附')

page('''
<h2>來源</h2>
<table class="t src">
<tr><th>來源</th><th>取得</th></tr>
<tr><td>Palmer &amp; Schloss 2010, PNAS 107:8877–8882</td><td>原文（palmerlab.berkeley.edu）</td></tr>
<tr><td>Schloss &amp; Palmer 2011, Atten Percept Psychophys 73:551–571</td><td>原文（Springer 開放取用）</td></tr>
<tr><td>Bae, Olkkonen, Allred &amp; Flombaum 2015, JEP: General 144(3)</td><td>原文（Allred 個人網頁，線上優先版）</td></tr>
<tr><td>Jonauskaite 等 2020, Psychological Science 31:1245–1260</td><td>作者接受稿（洛桑大學典藏，CC BY-NC-ND）</td></tr>
<tr><td>Ou 等 2004；Ou &amp; Luo 2006；Labrecque &amp; Milne 2012</td><td>付費牆，只讀摘要</td></tr>
<tr><td>Gramazio, Laidlaw &amp; Schloss 2017, Colorgorical</td><td>GitHub connorgr/colorgorical 9064965</td></tr>
<tr><td>Material Color Utilities</td><td>GitHub google/material-color-utilities dd62982</td></tr>
<tr><td>Radix Colors、Radix website</td><td>GitHub radix-ui/colors dbdb854、radix-ui/website 402e749</td></tr>
<tr><td>Adobe Leonardo</td><td>GitHub adobe/leonardo eb6481d</td></tr>
<tr><td>Munsell renotation、CIECAM02</td><td>GitHub colour-science/colour 248121e</td></tr>
<tr><td>Hirschler, Itten 七種對比批評</td><td>color-expert 知識庫逐字稿</td></tr>
<tr><td>和田三造、ISCC-NBS 色名</td><td>npm color-name-lists 3.34.0</td></tr>
<tr><td>Matsuda 模板（Cohen-Or 2006 實作）</td><td>GitHub tartarskunk/ColorHarmonization b789279</td></tr>
<tr><td>台灣同業 logo、車輛照片</td><td>你電腦崧淳同業logo資料夾；10-13 兩份台灣同業報告</td></tr>
<tr><td>香港渠務署、東京都水道局、台電、中油、中華電信車輛照片</td><td>維基共享資源：Negi（CC BY-SA 3.0）、Ypy31（CC0）、Solomon203（CC BY-SA 3.0）、玄史生（CC0）</td></tr>
<tr><td>美感串發現</td><td>崧淳CI/研究/23_LOGO與CIS美感學習_20261017/第二輪_20261018/第二輪學習筆記.md</td></tr>
</table>
''', '附')

# ---------- 輸出 ----------
out = ['<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>配色與設計理念・第二輪</title><style>', CSS, '</style></head><body>']
for i, (b, part, cls) in enumerate(pages, 1):
    foot = '' if 'nofoot' in cls else f'<div class="foot"><span>配色與設計理念・第二輪　{part}</span><span>{i}</span></div>'
    out.append(f'<section class="page {cls}"><div class="inner">{b}</div>{foot}</section>')
out.append('</body></html>')
open(R + 'report.html', 'w').write('\n'.join(out))
print('pages', len(pages))
