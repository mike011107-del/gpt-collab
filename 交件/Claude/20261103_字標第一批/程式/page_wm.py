import sys, os, pickle
W = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; FONTS = sys.argv[2]
R = pickle.load(open(os.path.join(OUT, 'res.pkl'), 'rb'))
css = open(os.path.join(W, '../work/style_common.css'), encoding='utf-8').read()
def sv(s, h): return s.replace('<svg ', f'<svg style="height:{h};width:auto;display:block;margin:0 auto" ', 1)
INFO = {
 'W1': dict(what='骨架是思源黑體 Black。每一筆的外角都切掉同樣大小的斜角，整組字只有直線和 45 度斜角，看起來像鋼板裁切、工程標示。兩字間距收緊到字寬的 5%。',
            why='切角讓字比原本的黑體硬、準，適合「做工程、講究細節」。最粗的一組，車門、遠距離最醒目。',
            changes=['所有外角切同一個角（切角寬約 24，字高 1000）', '崧：山的中豎高出 62', '兩字間距 46', '反白版每邊收細 5']),
 'W2': dict(what='骨架是思源宋體 Bold。保留明體橫細直粗的對比和三角收筆，兩字間距收緊到字寬的 3%。',
            why='粗細對比讓字看起來細緻、安靜，接近負責人「深色、低調、質感」的喜好〔推論〕。小尺寸時橫筆會變細，名片上要用大一點。',
            changes=['崧：山的中豎高出 64，筆端形狀沿用原字', '兩字間距 30', '反白版每邊收細 4']),
 'W3': dict(what='骨架是霞鶩文楷 Medium，整組加粗到接近現在車身的黑粗楷全名。',
            why='車隊已經在跑，換 LOGO 時車身跟新字標看起來是同一家，不會斷掉。楷書比較傳統，年輕感最弱。',
            changes=['整組筆畫每邊加粗 18', '崧：山的中豎高出 60，筆端形狀沿用原字', '兩字不留間距（楷書字面本身有空白）', '反白版每邊收細 6']),
}
def page(k):
    r = R[k]; i = INFO[k]
    px = ''.join(f'<div class="cell"><img src="{u}" style="height:9mm;image-rendering:pixelated"><div class="lab">{h}px</div></div>' for h, u in r['px'])
    ch = ''.join(f'<li>{c}</li>' for c in i['changes'])
    return f'''<h2 class="new">{k}　{r["name"]}</h2>
<div class="hero">{sv(r["main"], "32mm")}</div>
<p>{i["what"]}</p><p>{i["why"]}</p>
<div class="row two"><div class="cell"><div class="lab">原字型直接打</div>{sv(r["plain"], "12mm")}</div><div class="cell"><div class="lab">改過以後</div>{sv(r["main"], "12mm")}</div></div>
<div class="k">改了什麼</div><ul class="sm">{ch}</ul>
<div class="row two"><div class="cell">{sv(r["lock"], "22mm")}</div><div class="cell">{sv(r["rev"], "22mm")}</div></div>
<div class="k">縮小（實際像素，放大顯示）</div><div class="row px">{px}</div>'''
heroes = ''.join(f'<div class="cmp"><div class="tag">{k}　{R[k]["name"]}</div>{sv(R[k]["main"], "24mm")}</div>' for k in ('W1', 'W2', 'W3'))
html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>崧淳字標第一批</title>
<link rel="stylesheet" href="file://{FONTS}/400.css"><link rel="stylesheet" href="file://{FONTS}/700.css">{css}
<style>
.hero {{ margin: 3mm 0 4mm; }}
.cmp {{ margin: 0 0 5mm; padding-bottom: 3mm; border-bottom: 0.5pt solid #ddd; }}
.tag {{ font-weight: 700; font-size: 10pt; margin-bottom: 2mm; }}
.row.two {{ justify-content: space-between; align-items: flex-end; margin: 2mm 0 3mm; }}
.row.two .cell {{ width: 48%; }}
.row.px {{ gap: 6mm; align-items: flex-end; }}
.k {{ font-weight: 700; font-size: 9.5pt; margin: 2mm 0 1mm; }}
ul.sm li {{ font-size: 9.3pt; margin-bottom: 0.8mm; }}
p {{ font-size: 10pt; }}
</style></head><body>
<h1>崧淳字標　第一批</h1>
<div class="sub">三個骨架方向，黑白，2026-11-03<br>Claude 設計，給梁特助挑方向</div>
<p>這一批用來挑字標的「骨架」：黑體、明體、楷書三條路。三個方向共用同一個細節：崧字上方「山」的中豎高出一截。崧的字義是山大而高，這一截也對應「高標準」。只用一個細節，你比較的是骨架，不是花樣。</p>
<p>這是方向比較，不是定稿。你挑一個以後，才逐字修重心、中宮、每一筆粗細，再上色。</p>
{heroes}
{page("W1")}{page("W2")}{page("W3")}
<h2 class="new">檢查結果</h2>
<table class="vt"><tr><th>項目</th><th>W1</th><th>W2</th><th>W3</th></tr>
<tr><td>字寫對（崧不是松）</td><td>過</td><td>過</td><td>過</td></tr>
<tr><td>收筆一套規則</td><td>過，全部同一切角</td><td>過，沿用明體收筆</td><td>過，沿用楷書收筆</td></tr>
<tr><td>山中豎加高後還讀得出崧</td><td>過</td><td>過</td><td>過</td></tr>
<tr><td>反白版修細</td><td>過</td><td>過</td><td>過</td></tr>
<tr><td>16px 讀得出兩個字</td><td>過</td><td>部分，橫筆變淡</td><td>過</td></tr>
<tr><td>不用說明也成立</td><td>過</td><td>過</td><td>過</td></tr>
<tr><td>跟台灣同行字標並排</td><td>未比對</td><td>未比對</td><td>未比對</td></tr>
<tr><td>逐字精修（重心、中宮、粗細）</td><td>下一步</td><td>下一步</td><td>下一步</td></tr></table>
<p class="note">「未比對」：台灣同行的字標圖不在雲端資料夾，挑定方向後補。字標的字形來自開源字型（SIL OFL 1.1，可修改、可做 logo），要註冊商標前請律師看。英文名還沒有資料，這一批沒做。</p>
<h3>下一步</h3>
<ul><li>你挑一個方向，或說三個都不要、哪裡不對。挑定後我逐字精修，交第二版。</li>
<li>圖形：照新流程要先生黑白探索小圖。建議先試 AutoIP 1 張「一張圖 9 個小圖」（20 點），你同意我就生。</li></ul>
<h3>我替你做的判斷</h3>
<ul><li>把你說的「去查找相關資源替我設計」當成同意用開源字型當骨架：FedEx 也是從現成字體改起，這樣最快有東西給你看。</li>
<li>三個方向只用一個共同細節（山中豎），讓你比骨架，不被花樣影響。</li>
<li>業務行照現有工項寫「污水下水道清淤・CCTV檢視」，沒有自己改寫。</li>
<li>先黑白，不上色；11-03 定的四色等方向挑定再套。</li></ul>
</body></html>'''
open(os.path.join(OUT, 'wm.html'), 'w', encoding='utf-8').write(html)
print('ok')
