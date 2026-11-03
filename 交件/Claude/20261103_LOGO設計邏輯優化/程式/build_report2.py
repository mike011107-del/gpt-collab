"""LOGO 設計邏輯優化報告：產生 report2.html（再由 pdf.js 印成 A5 PDF）。
用法：python3 -I build_report2.py <work 資料夾> <fonts package 資料夾> <simple-icons icons 資料夾>
"""
import os, re, sys

W, FONTS, SI = sys.argv[1], sys.argv[2], sys.argv[3]
IMG = os.path.join(W, 'img')


def read(p):
    return open(p, encoding='utf-8').read()


def si(name, size='16mm', fill='#111111'):
    s = read(os.path.join(SI, name + '.svg'))
    s = re.sub(r'<title>.*?</title>', '', s)
    return s.replace('<svg ', f'<svg style="width:{size};height:{size}" fill="{fill}" ', 1)


def inline_svg(name, cls='figs'):
    s = read(os.path.join(IMG, name))
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    s = re.sub(r'<svg ', f'<svg class="{cls}" ', s, count=1)
    return re.sub(r' width="[0-9.]+" height="[0-9.]+"', '', s, count=1)


def board(items, size='15mm', per='23%'):
    cells = ''.join(
        f'<div class="cell" style="width:{per}"><div class="box">{si(n, size)}</div><div class="lab">{lab}</div></div>'
        for n, lab in items)
    return f'<div class="row">{cells}</div>'


FIG_WORD = f'''<figure>
{board([('siemens', '西門子'), ('hitachi', '日立'), ('toshiba', '東芝'), ('epson', 'Epson'),
        ('fedex', 'FedEx'), ('samsung', 'Samsung'), ('panasonic', 'Panasonic'), ('3m', '3M'),
        ('abb', 'ABB'), ('caterpillar', 'Caterpillar'), ('sony', 'Sony'), ('kyocera', 'Kyocera')], '20mm')}
<figcaption>圖 2　國外大廠字標。看起來都像「粗體字」，但沒有一個是直接打字。外部標誌取自 simple-icons 16.35.0（單色版）。</figcaption></figure>'''

FIG_SYM = f'''<figure>
{board([('mitsubishi', '三菱<br>一個菱形轉三次'), ('chase', 'Chase<br>一塊形狀轉四次'), ('deutschebank', '德意志銀行<br>方框裡一條斜線'), ('volkswagen', 'VW<br>兩個字母疊成一個形'),
        ('lufthansa', 'Lufthansa<br>一隻鶴，線條收緊'), ('deutschepost', '德國郵政<br>號角簡化成剪影'), ('shell', 'Shell<br>貝殼簡化成剪影'), ('chinarailway', '中國鐵路<br>人字在鋼軌上'),
        ('toyota', 'Toyota<br>三個橢圓'), ('bosch', 'Bosch<br>圓裡一個電樞'), ('mastercard', 'Mastercard<br>兩個重疊的圓'), ('scania', 'Scania<br>對照：細節多')], '16mm')}
<figcaption>圖 4　大廠圖形標各用一個構成方法。最後一個 Scania 的獅鷲細節多，縮小後只剩一團，是反例。外部標誌取自 simple-icons 16.35.0。</figcaption></figure>'''

FIG_CN = f'''<figure>
{board([('meituan', '美團<br>整組字標'), ('xiaohongshu', '小紅書<br>整組字標，斜、等粗'), ('taobao', '淘寶<br>整組字標，粗細對比強'), ('uniqlo_ja', 'UNIQLO<br>片假名畫成方塊'),
        ('alipay', '支付寶<br>「支」畫成符號'), ('douban', '豆瓣<br>「豆」畫成符號'), ('zhihu', '知乎<br>「知」加對話框'), ('airchina', '國航<br>不是字的圖形')], '17mm')}
<figcaption>圖 1　大品牌的中文字 LOGO。上排是整組字訂製的字標，下排是一個字畫成符號，或配一個不是字的圖形。外部標誌取自 simple-icons 16.35.0（單色版）。</figcaption></figure>'''

RATIO = [
    ('日立 HITACHI', '「H」', '65', '40', '0.62'),
    ('西門子 SIEMENS', '「E」', '66', '42～49', '0.64～0.74'),
    ('東芝 TOSHIBA', '「O」', '67', '55', '0.82'),
    ('Epson', '「E」', '76', '64～65', '0.84～0.86'),
    ('美團', '「美團」', '68～72', '52～56', '0.72～0.82'),
    ('淘寶', '「淘寶」', '104～124', '48～52', '約 0.4～0.5'),
    ('小紅書', '「小紅書」', '104～108', '104', '約 1.0'),
    ('思源黑體 Bold', '「崧淳」', '68～76', '58～64', '0.80～0.87'),
    ('崧淳 G1 到 G3', '「崧淳」', '24', '24', '1.00'),
]
FIG_RATIO = '<figure><table class="mini"><tr><th>字標</th><th>量的字</th><th>直筆</th><th>橫筆</th><th>橫÷直</th></tr>' + ''.join(
    f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td><b>{e}</b></td></tr>' for a, b, c, d, e in RATIO) + \
    '</table><figcaption>圖 3　Claude 11-03 把 simple-icons 的字標放大到 1600px 後掃描像素量的（單位是像素，各標誌大小不同，只比比值）。看起來等粗的西文字標，橫筆也比直筆細 15% 到 38%。中文字標從 0.4 到 1.0 都有：粗細比沒有標準答案，小紅書幾乎等粗也成立，因為收筆、轉角、斜度全組一致。G1 到 G3 的問題不在 1.00 這個數字，在於等粗之外什麼修正都沒做。</figcaption></figure>'

OLDNEW = [
    ('出發點', '「崧」字裡有山，就畫山', '先寫一句「誰、在哪裡、第一眼認出什麼」；做的事交給字標和業務行，圖形求合適'),
    ('探索量', '3 個方向就交件', '數十個黑白小圖，收斂成 6 到 9 個給你挑'),
    ('顏色', '先定四色怎麼放', '先黑白剪影，挑定方向才上色'),
    ('字標', '程式拼等寬直線，方頭、尖角、沒有收筆', '骨架照第六節選的方式；粗細風格刻意選定；收筆、轉角、交接一套規則；逐字調大小重心、逐對調字距'),
    ('圖形', '用字（山）當圖形', '一個構成方法；看一兩次就畫得出來；任何尺寸都能用'),
    ('檢查', '縮小、反白、車身三項量測', '加上同業並排、憑記憶畫、Rand 七條、PR #49 的 14 條對照表'),
    ('誰畫', 'Claude 自己畫完交', '圖形草圖交 AutoIP／GPT（不放中文字）；字標照第五節你選的方式；Claude 寫交辦、篩選、驗收'),
]
FIG_OLDNEW = '<table class="vt"><tr><th>項目</th><th>這次的做法</th><th>改成</th></tr>' + ''.join(
    f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in OLDNEW) + '</table>'

html = read(os.path.join(W, 'report2_body.html'))
STYLE = read(os.path.join(W, 'style_common.css'))
for k, v in dict(STYLE=STYLE, FIG_CN=FIG_CN, FIG_WORD=FIG_WORD, FIG_SYM=FIG_SYM, FIG_RATIO=FIG_RATIO, FIG_OLDNEW=FIG_OLDNEW, FONTS=FONTS).items():
    html = html.replace('{{' + k + '}}', v)
left = re.findall(r'\{\{[A-Z_0-9]+\}\}', html)
assert not left, left
open(os.path.join(W, 'report2.html'), 'w', encoding='utf-8').write(html)
print('report2.html', len(html))
