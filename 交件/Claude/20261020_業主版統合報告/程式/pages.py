T = P['teal']; I = P['indigo']; Y = P['shared']

# 1 封面
page(f'''
<div class="cover-img"><img src="i/sc3.jpg"></div>
<div class="cover-text">
<div class="cbar"><div style="flex:1;background:#0C424A"></div><div style="flex:1;background:#333D66"></div><div style="flex:0.7;background:#D68702"></div></div>
<div class="ct">崧淳環保科技<br>企業識別主視覺色　研究與候選報告</div>
<div class="cs">車身工程黃已定。主色有兩個候選：深青、靛藍。<br>本報告把兩個顏色的事實並列，請業主選一個。</div>
<div class="cm">對象：崧淳環保科技股份有限公司<br>日期：2026 年 10 月 20 日<br>範圍：企業識別主視覺色（主色、輔色、色碼規格、使用原則）；宣傳語候選；標誌與標準字的設計原則。不含標誌設計稿，不改車身顏色。<br>封面照片：崧淳吸污車，業主提供。</div>
</div>''')

# 2 一頁看完
page(f'''
<div class="part">一頁看完</div>
<h2>要請您決定的只有一件事：主色用深青，還是靛藍</h2>
<p class="lead">車身的工程黃不變，當輔色。主色負責讓人記住崧淳。兩個候選都通過基本的可讀性檢查，差別在「跟誰像」與「看起來的感覺」。</p>
<div class="cand">
 <div><div class="chip" style="background:#0C424A"><div class="nm">A　深青</div><div class="hx">#0C424A　Pantone 316 C 附近</div><div class="yl"></div></div></div>
 <div><div class="chip" style="background:#333D66"><div class="nm">B　靛藍</div><div class="hx">#333D66　Pantone 5265 C 附近</div><div class="yl"></div></div></div>
</div>
<table class="facts">
<tr><th></th><th>A 深青</th><th>B 靛藍</th></tr>
<tr><td>台灣同業最像的</td><td>華通衛生行的青 #005959，色差 9.3</td><td>大亞的深藍 #243952，色差 7.0</td></tr>
<tr><td>國外同業最像的</td><td>Ventia #004127，色差 16.7</td><td>Insituform #102E68，色差 6.7</td></tr>
<tr><td>在台灣同業裡屬於</td><td>青、綠之間，少數</td><td>藍，台灣同業最多的一類（17 家中 9 家）</td></tr>
<tr><td>白字放在上面</td><td>亮度比 11.1，很清楚</td><td>亮度比 10.5，很清楚</td></tr>
<tr><td>工程黃放在上面</td><td>亮度比 3.9，只適合大字和色塊</td><td>亮度比 3.7，只適合大字和色塊</td></tr>
<tr><td>兩色差多少</td><td colspan="2">色差 20.1，並排一看就分得出來</td></tr>
</table>
<p class="note">色差（CIEDE2000）：數字越小越像。本報告把 10 以內當作「容易被看成同一類顏色」，這是工作用的界線，不是標準。亮度比：數字越大越清楚，一般內文要 4.5 以上，大字 3 以上（WCAG 2）。</p>
<div class="box k"><h3>另外兩件事</h3>
<ol><li>宣傳語有四句候選（第 17 頁），尚未定案。</li>
<li>要請業主提供：實際的工程資料或作業照片、是否已有任何標誌或字樣草稿。標誌要等主色定了再做。</li></ol></div>
''')

# 3 崧淳現況
page(f'''
<div class="part">一　崧淳現在的樣子</div>
<h2>車隊是整台工程黃，車上只有黑色全名，還沒有標誌</h2>
<div class="g2"><figure><img class="h" src="i/sc1.jpg"><div class="cap">車隊全景。吸污車與廂型車同一個黃。</div></figure>
<figure><img class="h" src="i/sc2.jpg"><div class="cap">作業中。三角錐與車身都是暖色。</div></figure></div>
<div class="g2" style="margin-top:2mm">
<div>
<h3>工程黃：從照片量出來的車身色</h3>
<p><span class="sw" style="background:#D68702"></span><b>#D68702</b>　CMYK {'/'.join(map(str,Y['yellow']['cmyk']))}　Pantone 131 C 附近（色差 0.9）　RAL 1006 附近（色差 3.1）</p>
<p>過去幾份文件裡出現過四個黃：#D68702、#D58401、#F3B51B、#FACA30。前兩個都是從車身照片量的（不同天、不同照片），差 1.0，看不出來；後兩個跟車身差 13.7 和 19.5，是不同的黃。<b>本報告一律用 #D68702。</b></p>
<p class="note">照片量的顏色受光線影響。做招牌、印刷前，要拿車身的實際烤漆跟色票本比對一次。</p>
</div>
<div>
<h3>這代表什麼</h3>
<ul><li>車身顏色不改，所以主色只能出現在標誌、招牌、文件、制服、網站，以及車上的標誌位置。</li>
<li>黃車在台灣路上不稀奇（第 5 頁），單靠黃色認不出是崧淳。讓人記住的工作要交給主色和標誌。</li>
<li>工程黃上面放白字只有 2.87，太淡；放墨色字有 5.05，夠清楚。車身上的字要用深色。</li></ul>
</div></div>
''')

# 4 台灣同業 1
page(f'''
<div class="part">二　台灣同業</div>
<h2>21 家同業：一半只用一個顏色，藍綠最多，沒有人用紅</h2>
<div class="g2" style="grid-template-columns:1.05fr 1fr">
<figure><img src="i/fig_tw_logo_grid_v3.png" style="border:0.4pt solid #ddd"><div class="cap">21 家同業的標誌（取自公開網頁、商標圖樣與業主提供的資料夾）。標誌為各公司所有，只供比較。</div></figure>
<div>
<h3>逐張量色的結果</h3>
<ul>
<li><b>只用一個顏色加黑白：</b>20 家中 10 家（順捷是黑色商標，不計）。國外 48 家是 23 家，比例差不多。</li>
<li><b>主色：</b>有彩色的 17 家裡，藍 9、綠 6、橘 1、黃 1。<b>沒有紅，也幾乎沒有青。</b></li>
<li><b>標誌圖形：</b>21 家裡只有字的 6 家，水滴水波 5 家，箭頭循環 4 家，管子 3 家。10 月 11 日看的 14 家，宣傳語多是「經驗豐富、專業、快速」。</li>
<li><b>兩色標誌的深淺差：</b>台灣用兩色的 7 家裡，華通、日技兩家兩色幾乎一樣深，轉黑白會糊。整體深淺差中位數台灣 19.7、國外 32.1，但台灣只有 7 家，還不能確定差在哪。</li>
</ul>
<figure><img src="i/fig_scheme_compare_v3.png"><div class="cap">配色方式占比：台灣 20 家對國外 48 家，同一支程式分組。</div></figure>
</div></div>
<p class="note">量色方法：每張標誌去掉白底，統計各色面積；色相分類用 OKLCH。逐張數字在附錄提到的研究資料裡。</p>
''')

# 5 台灣同業 2 車
page(f'''
<div class="part">二　台灣同業</div>
<h2>黃色、橘色的槽車在台灣不少，黃色本身不是崧淳獨有</h2>
<div class="g2">
<figure><img class="h" src="i/tw_honglong.jpg"><div class="cap">宏隆：黃色槽體。標誌主色是綠。照片：業主電腦同業資料夾。</div></figure>
<figure><img class="h" src="i/tw_yiyuan.jpg"><div class="cap">一元：淡黃車身。標誌主色是藍。照片：業主電腦同業資料夾。</div></figure>
<figure><img class="h" src="i/v_taipower.jpg"><div class="cap">台電：整排黃色工程車。Solomon203，維基共享資源，CC BY-SA 3.0。</div></figure>
<figure><img class="h" src="i/v_cht.jpg"><div class="cap">中華電信：黃色公務車。Solomon203，維基共享資源，CC BY-SA 3.0。</div></figure>
</div>
<ul>
<li>21 家同業裡，宏隆、日技、派浦崴洱、一元 4 家是黃或橘的槽車；台電、中華電信的工程車也是黃色。路人看到黃車，先想到的可能是「工程車」，不一定是哪一家（推論）。</li>
<li>車身跟標誌同色系的只看到華通（綠槽配綠標誌）。其他家的車色跟標誌色各走各的。</li>
<li>所以崧淳的組合是「黃車＋自己的主色標誌」。主色要在黃車上站得住，也要跟這些同業標誌分得開。</li>
</ul>
''')

# 6 國外同業 1
page(f'''
<div class="part">三　國外同業</div>
<h2>國外 48 家：一半只用一個顏色，藍最多，紅其次</h2>
<p class="lead">涵蓋英、德、法、日、美、澳等地的環境集團、水務、清管、管線修復與設備廠。從標誌檔、官網與車隊照片量色。</p>
<figure><img src="i/fig_hue_ring_v3.png"><div class="cap">每家主色在色相環上的位置：左為國外 42 家，右為台灣 17 家（只列有彩色主色的）。</div></figure>
<div class="g2">
<div><h3>看到的規律</h3><ul>
<li>48 家有 23 家只用一個彩色加黑白灰，例如 Veolia 的紅、Biffa 的紅、Lanes 的粉紅。</li>
<li>有彩色主色的 42 家中，紅占 11 家。台灣同業沒有紅，國外常見。</li>
<li>深青附近（#0C424A 色差 15 以內）國外沒有品牌；最近的是 Ventia 16.7。</li>
</ul></div>
<div><h3>要小心的地方</h3><ul>
<li>這 48 家是大品牌，不代表各國所有小型清管公司。</li>
<li>取色來自網頁與照片，跟印刷色票會有落差。</li>
<li>國外沒人用的顏色，不代表在台灣也沒人用：深青在國外是空的，在台灣有華通衛生行的 #005959（第 11 頁）。</li>
</ul></div></div>
''')

# 7 國外車隊
page(f'''
<div class="part">三　國外同業</div>
<h2>車隊有兩種做法：整台漆品牌色，或白車加大字</h2>
<div class="g3">
<figure><img class="h" src="i/Biffa_c13.jpg"><div class="cap">Biffa：紅車、白字，沒有第三個顏色。</div></figure>
<figure><img class="h" src="i/Kanal-Tuerpe_c29.jpg"><div class="cap">Kanal-Türpe（德國清管）：據點、清淤車、廂型車同一個橘。</div></figure>
<figure><img class="h" src="i/Lanes_Group_c31.jpg"><div class="cap">Lanes Group：清淤車和廂型車都是粉紅。</div></figure>
<figure><img class="h" src="i/Thames_Water_c01.jpg"><div class="cap">Thames Water：白車，藍色標誌與字，車側一條格紋帶。</div></figure>
<figure><img class="h" src="i/Roto-Rooter_c01.jpg"><div class="cap">Roto-Rooter：白車一字排開，全員同款制服。</div></figure>
<figure><img class="h" src="i/v_tokyo.jpg"><div class="cap">東京都水道局：白車加一條藍帶。Ypy31，CC0。</div></figure>
</div>
<div class="box k"><h3>跟崧淳的關係</h3>
<p>崧淳屬於第一種：整台車已經是一個顏色（工程黃）。照片裡這一派的車，多半只再放一個顏色或黑白（推論，沒有逐家計數）。香港渠務署的吸渠車也是整台黃，標誌只在車門上一小塊。</p>
<p style="margin:0">推論：崧淳的主色在車上應該只出現在標誌那一塊，車身其他地方維持黃加深色字。</p></div>
<p class="cap">國外照片取自各公司官網與公開新聞稿，只供比較，著作權屬原公司。</p>
''')

# 8 現場與制服
page(f'''
<div class="part">三　國外同業</div>
<h2>到了工地，多半穿橘或螢光黃反光衣，品牌靠背上和胸前的標誌</h2>
<div class="g2">
<figure><img class="h" src="i/Kier_c08.jpg"><div class="cap">Kier（英國營造）：螢光黃反光背心，背後大字標誌。</div></figure>
<figure><img class="h" src="i/Remondis_c04.jpg"><div class="cap">REMONDIS（德國）：橘色反光工作服。</div></figure>
<figure><img class="h" src="i/Tideway_c05.jpg"><div class="cap">Tideway（倫敦下水道隧道）：橘、青綠兩色反光衣。</div></figure>
<figure><img class="h" src="i/Metawater_c09.jpg"><div class="cap">メタウォーター（日本）：藍色制服、白安全帽。官網形象圖。</div></figure>
</div>
<ul>
<li>工地安全規定讓工作服多半是橘或螢光黃，品牌色很難放大。標誌要在小面積、反光布上也認得出來。</li>
<li>辦公室與業務場合（名片、報價單、網站、制服 Polo 衫）才是主色的大面積用途。</li>
<li>主色選得太淺或太鮮，印在反光布上會跟底色搶；兩個候選都是深色，這點應該都沒問題（推論）。</li>
</ul>
''')

# 9 原則
page(f'''
<div class="part">四　好的企業識別怎麼管顏色</div>
<h2>大公司的手冊都規定：同一個畫面只用少數幾個顏色</h2>
<div class="g3">
<figure><img src="i/veolia_p7_palette.jpg" style="height:64mm;object-fit:contain;border:0.4pt solid #ddd"><div class="cap">Veolia 品牌手冊色彩頁：紅、白、黑固定；同一頁建議最多兩色，可另加黑白。</div></figure>
<figure><img src="i/nasa_colour.jpg" style="height:64mm;object-fit:contain;border:0.4pt solid #ddd"><div class="cap">NASA 1975 年手冊：只有 NASA 紅、NASA 暖灰兩色。</div></figure>
<figure><img src="i/epa_agency.jpg" style="height:64mm;object-fit:contain;border:0.4pt solid #ddd"><div class="cap">美國環保署 1977 年手冊：機關色（EPA 藍、綠）與各業務色分兩層。</div></figure>
</div>
<h3>從這些手冊整理出的四條原則</h3>
<ol>
<li><b>一個主色就夠。</b>國外大品牌與台灣同業，都約一半只用一個顏色加黑白。</li>
<li><b>大面積用白，主色是重點，不是背景。</b>建議書的參考比例是白 60、主色 25、灰 10、黃 5（第 16 頁）。</li>
<li><b>顏色要先定色號，再定用法。</b>手冊都把 Pantone、CMYK、RGB 與「不准怎麼用」寫清楚。</li>
<li><b>車身顏色不改也能成套。</b>NASA 1975 只管標誌的位置、大小與黑白反轉。崧淳可以照這個做法，只規定車門標誌與車身字的位置和大小。</li>
</ol>
''')

# 10 工程黃規則
page(f'''
<div class="part">五　輔色：工程黃</div>
<h2>工程黃已定，用法要先講好：黃底配深字，不要配白字</h2>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin-bottom:2mm"><div><div style="height:28mm;background:#0C424A;border:0.4pt solid #ccc;display:flex;align-items:center;justify-content:center"><div style="width:11mm;height:11mm;background:#D68702"></div></div><div class="cap" style="font-size:8.4pt;color:#333">深青 #0C424A<br>亮度比 3.87<br>看起來多亮 59.0</div></div><div><div style="height:28mm;background:#333D66;border:0.4pt solid #ccc;display:flex;align-items:center;justify-content:center"><div style="width:11mm;height:11mm;background:#D68702"></div></div><div class="cap" style="font-size:8.4pt;color:#333">靛藍 #333D66<br>亮度比 3.66<br>看起來多亮 58.7</div></div><div><div style="height:28mm;background:#FFFFFF;border:0.4pt solid #ccc;display:flex;align-items:center;justify-content:center"><div style="width:11mm;height:11mm;background:#D68702"></div></div><div class="cap" style="font-size:8.4pt;color:#333">白 #FFFFFF<br>亮度比 2.87<br>看起來多亮 46.1</div></div><div><div style="height:28mm;background:#777777;border:0.4pt solid #ccc;display:flex;align-items:center;justify-content:center"><div style="width:11mm;height:11mm;background:#D68702"></div></div><div class="cap" style="font-size:8.4pt;color:#333">中灰 #777777<br>亮度比 1.56<br>看起來多亮 55.1</div></div><div><div style="height:28mm;background:#000000;border:0.4pt solid #ccc;display:flex;align-items:center;justify-content:center"><div style="width:11mm;height:11mm;background:#D68702"></div></div><div class="cap" style="font-size:8.4pt;color:#333">黑 #000000<br>亮度比 7.33<br>看起來多亮 61.0</div></div></div><p class="cap" style="margin-bottom:3mm">同一個工程黃放在五種底上。「看起來多亮」是色彩模型（CIECAM02）的預測值，數字越大越亮；模型不算色相偏移。</p>
<table>
<tr><th>組合</th><th class="n">亮度比</th><th>可以做什麼</th></tr>
<tr><td><span class="sw" style="background:#D68702"></span>墨色字 #222B2C 在工程黃上</td><td class="n">5.05</td><td>車身文字、黃底告示，內文也可以</td></tr>
<tr><td><span class="sw" style="background:#D68702"></span>白字在工程黃上</td><td class="n">2.87</td><td>不夠，避免</td></tr>
<tr><td><span class="sw" style="background:#0C424A"></span>工程黃在深青上</td><td class="n">3.87</td><td>大字、線條、色塊；小字不行</td></tr>
<tr><td><span class="sw" style="background:#333D66"></span>工程黃在靛藍上</td><td class="n">3.66</td><td>大字、線條、色塊；小字不行</td></tr>
<tr><td><span class="sw" style="background:#04272C"></span>工程黃在深青的深階上</td><td class="n">5.50</td><td>可以放小字</td></tr>
<tr><td><span class="sw" style="background:#192039"></span>工程黃在靛藍的深階上</td><td class="n">5.60</td><td>可以放小字</td></tr>
</table>
<ul>
<li>工程黃當輔色時面積要小：一條線、一個重點框、車身本身。印刷品上不要整面鋪黃。</li>
<li>放在深色底上，黃看起來會比在白底上更亮（模型預測：深青底 59.0、靛藍底 58.7、白底 46.1）。</li>
<li>推論：深青底會讓黃略偏紅橘，靛藍底會讓黃略偏黃；偏多少這個模型算不出來，要看實物。</li>
</ul>
''')

def cand_page(key, name, hx, txt_peer, imgs, extra):
    d = P[key]
    return f'''
<div class="big" style="background:{hx}"><div class="nm">{name}</div><div class="hx">{hx}　RGB {','.join(map(str,d['primary']['rgb']))}　CMYK {'/'.join(map(str,d['primary']['cmyk']))}<br>Pantone {d['primary']['pantone'][0]} 附近（色差 {d['primary']['pantone'][1]}）　RAL {d['primary']['ral'][0][4:]} 附近（色差 {d['primary']['ral'][2]}）</div><div class="yl"></div></div>
{txt_peer}
{imgs}
{extra}'''

# 11 候選 A
page('<div class="part">六　主色候選 A</div><h2>深青：在台灣同業裡少見，但不是沒人用</h2>' + cand_page('teal', 'A　深青', '#0C424A', '''
<div class="g2"><div>
<h3>事實</h3>
<table class="facts">
<tr><td>色相</td><td>青，偏綠一點（Munsell 0.6B）</td></tr>
<tr><td>深淺</td><td>很深（Munsell 明度 2.5 / 10）</td></tr>
<tr><td>鮮度</td><td>彩度 3.7，比國外 42 家主色都低；但同深淺下已接近螢幕能做到的上限（0.91）</td></tr>
<tr><td>白字</td><td>亮度比 11.09</td></tr>
</table></div>
<div><h3>跟誰像（色差）</h3>
<table class="facts">
<tr><td><span class="sw" style="background:#005959"></span>華通衛生行</td><td><b>9.3</b>　台灣最近</td></tr>
<tr><td><span class="sw" style="background:#243952"></span>大亞</td><td>14.0</td></tr>
<tr><td><span class="sw" style="background:#004127"></span>Ventia</td><td>16.7　國外最近</td></tr>
<tr><td><span class="sw" style="background:#205C42"></span>Murphy</td><td>17.6</td></tr>
<tr><td><span class="sw" style="background:#007B86"></span>Kier</td><td>19.1　Kier 的青綠次色（主色是紅）</td></tr>
</table></div></div>
<div class="box"><b>要注意：</b>深青在台灣不是沒人用。同業華通的主標誌是綠，但它另一個據點「華通衛生行」的字樣用 #005959，跟深青差 9.3。先前文件若寫「同行沒有人用深青」，以這裡為準。</div>''',
'''<div class="g2"><figure><img class="h" src="i/fascia_teal.jpg" style="height:46mm"><div class="cap">示意：AI 生成的空白街景，招牌色塊用程式貼上準確色碼。不是設計稿。</div></figure>
<figure><img class="h" src="i/Murphy_c01.jpg" style="height:46mm;object-position:50% 70%"><div class="cap">實景參考：Murphy（英國營造）綠色車身；它的標誌綠 #205C42 跟深青差 17.6。</div></figure></div>''', ''))

# 12 候選 B
page('<div class="part">六　主色候選 B</div><h2>靛藍：落在台灣同業最多的藍色區，跟大亞很近</h2>' + cand_page('indigo', 'B　靛藍', '#333D66', '''
<div class="g2"><div>
<h3>事實</h3>
<table class="facts">
<tr><td>色相</td><td>藍，偏紫一點（Munsell 7.0PB）；OKLCH 色相 272，仍在藍的範圍（225–285），不是紫</td></tr>
<tr><td>深淺</td><td>很深（Munsell 明度 2.7 / 10）</td></tr>
<tr><td>鮮度</td><td>彩度 5.7；同深淺下只到螢幕上限的 0.30，比 42 家國外同業主色都灰。觀感偏灰、沉穩（主觀）</td></tr>
<tr><td>白字</td><td>亮度比 10.50</td></tr>
</table></div>
<div><h3>跟誰像（色差）</h3>
<table class="facts">
<tr><td><span class="sw" style="background:#243952"></span>大亞</td><td><b>7.0</b>　台灣最近</td></tr>
<tr><td><span class="sw" style="background:#255092"></span>一元</td><td>10.1</td></tr>
<tr><td><span class="sw" style="background:#2368AD"></span>天福</td><td>18.2</td></tr>
<tr><td><span class="sw" style="background:#102E68"></span>Insituform</td><td><b>6.7</b>　國外最近（管線修復）</td></tr>
</table></div></div>
<div class="box">大亞的 #243952 取自大亞標誌裡槽車圖形漸層較深的一端；大亞標誌面積最大的是黑色，藍是次色。靛藍跟它差 7.0，屬於「容易被看成同一類」。</div>''',
'''<div class="g2"><figure><img class="h" src="i/fascia_indigo.jpg" style="height:46mm"><div class="cap">示意：同一張 AI 街景，換成靛藍。不是設計稿。</div></figure>
<figure><img class="h" src="i/Rioned_c29.jpg" style="height:46mm"><div class="cap">實景參考：Rioned（荷蘭清管設備）藍色廂型車。</div></figure></div>''', ''))

# 13 並排
def mock(key, hx):
    d = P[key]
    ink = d['ink']['hex']
    return f'''<div>
<div class="card" style="background:#fff"><div class="ln" style="top:0;background:{hx};height:9mm"></div><div class="ln" style="top:9mm"></div><div class="s" style="color:#555">污水下水道清淤　管線 CCTV 檢視</div><div class="t" style="color:{hx}">崧淳環保科技股份有限公司</div></div>
<div class="cap" style="margin-bottom:3mm">名片／文件抬頭：白底，主色只在上緣，黃一條細線。</div>
<div class="card" style="background:{hx};border:none"><div class="s" style="color:#fff;opacity:.85">污水下水道清淤　管線 CCTV 檢視</div><div class="t" style="color:#fff">崧淳環保科技股份有限公司</div><div class="ln" style="bottom:0"></div></div>
<div class="cap" style="margin-bottom:3mm">主色當底：白字。黃只放在邊緣。</div>
<div class="door"><div style="position:absolute;left:5mm;top:6mm;width:9mm;height:9mm;background:{hx}"></div><div class="t" style="color:{ink};left:17mm;top:6.5mm">崧淳環保科技</div><div class="s" style="color:{ink};left:17mm;top:13.5mm">污水下水道清淤　CCTV 檢視</div></div>
<div class="cap">車門：車身黃不變，標誌位置放主色，字用墨色。</div>
</div>'''

page(f'''
<div class="part">七　兩色並排</div>
<h2>放在同樣的地方比一比</h2>
<p class="note">以下是用色塊排的示意，不是標誌設計。字用一般黑體暫代，不是崧淳的標準字；方塊只標出標誌的位置。</p>
<div class="g2"><div><h3>A 深青</h3>{mock('teal','#0C424A')}</div><div><h3>B 靛藍</h3>{mock('indigo','#333D66')}</div></div>

''')

# 14 規格 A
page(f'''
<div class="part">八　色碼規格</div>
<h2>A 深青　整組色碼</h2>
{scale('teal')}
<p class="cap" style="margin-bottom:3mm">主色往深、往淺展開，色相固定。</p>
{spec_table('teal')}
<p class="note">CMYK 是用一般印刷描述檔（Ghostscript default_cmyk.icc、相對色度）換算的參考值；Pantone、RAL 是從公開色表找最近的一號，後面的數字是色差。<b>實際印刷與烤漆一定要拿色票打樣確認。</b>對白底亮度比低於 4.5 的顏色（淺階、淺灰、霧白，以及冷灰）不要拿來當白底上的小字。深階、淺階離 RAL 色號也遠（色差 7 以上），烤漆要調色。白色是紙白，不必印。</p>
''')

# 15 規格 B
page(f'''
<div class="part">八　色碼規格</div>
<h2>B 靛藍　整組色碼</h2>
{scale('indigo')}
<p class="cap" style="margin-bottom:3mm">主色往深、往淺展開，色相固定（OKLCH 色相 272）。淺階、墨色是配合靛藍另外選的。</p>
{spec_table('indigo')}
<p class="note">換算方法同上一頁。靛藍的淺階 #B6C5DF 在 RAL 色表裡找不到相近的（最近 RAL 7047 差 11.9），烤漆要用調色，不能直接叫 RAL 色號。</p>
''')

# 16 使用規則
page(f'''
<div class="part">九　使用原則</div>
<h2>選定主色後，照這幾條用</h2>
<div class="g2">
<div><h3>面積比例（參考）</h3>
<div style="display:flex;height:14mm;margin-bottom:1mm;border:0.4pt solid #ddd"><div style="flex:60;background:#fff"></div><div style="flex:25;background:#0C424A"></div><div style="flex:10;background:#788284"></div><div style="flex:5;background:#D68702"></div></div>
<div style="display:flex;height:14mm;margin-bottom:1.5mm;border:0.4pt solid #ddd"><div style="flex:60;background:#fff"></div><div style="flex:25;background:#333D66"></div><div style="flex:10;background:#7D8088"></div><div style="flex:5;background:#D68702"></div></div>
<p class="cap">白 60、主色 25、灰 10、工程黃 5。這是建議書提的起點，不是規定；車身不在此限。</p></div>
<div><h3>文字</h3><ul>
<li>白底上的字：主色或墨色。</li>
<li>主色底上的字：白。</li>
<li>工程黃底上的字：墨色，不用白。</li>
<li>工程黃當字：只在主色深階上，或當大標題。</li></ul></div></div>
<h3>車身</h3>
<ul>
<li>車身黃不改。車門放「標誌＋公司名」的小字，車廂或罐體放大字名稱，兩層大小差 2.5 到 7 倍（國內外公務車照片估的量級）。</li>
<li>遠看的字高：每 1 公分字高，理想狀況約可在 3.6 公尺外讀到（美國招牌協會 USSC 平均值）；開車時至少打六五折，約 2.3 公尺。例如要在 50 公尺外讀到，字高約 22 公分。</li>
<li>黃車身上用深色字；反白字只放在另外加的主色色塊裡。</li>
</ul>
<h3>不要做的事</h3>
<ul>
<li>不要同時用深青和靛藍。選定一個，另一個就不用了。</li>
<li>不要把主色調亮、調鮮來「更醒目」；要醒目時用工程黃當小面積重點。</li>
<li>不要在主色上加漸層、陰影、發光。我們看到的大品牌手冊多是平塗。</li>
</ul>
''')

# 17 slogan
page(f'''
<div class="part">十　宣傳語候選</div>
<h2>四句候選，尚未定案</h2>
<p class="lead">條件：句中要有「崧淳」（可以拆開放在上下句）；一聽就知道是做清淤或管線檢視；要對仗或有反差；不要套話。</p>
<div class="sl"><div class="pull">崧淳把淤泥全帶走，把裂縫全留下。</div><p class="note" style="margin:0">主推。前半講清淤，後半講 CCTV 檢視：裂縫一條不漏留在影片和報告裡。念到「裂縫全留下」會愣一下，想一下才懂。風險：可能被誤讀成「不修裂縫」，用在名片時下面要接公司全名和業務。</p></div>
<div class="sl"><div class="pull">電影一鏡到底，為了拿獎；崧淳一鏡到底，為了驗收。</div><p class="note" style="margin:0">國土署的 CCTV 規範要求檢視連續、不得中斷或剪接。同一個「一鏡到底」，電影拿來炫技，這行是規範。句子長，適合投標簡報、影片片頭。</p></div>
<div class="sl"><div class="pull">崧淳天天下水，從不拖人下水。</div><p class="note" style="margin:0">前面是真的下到下水道，後面是把人拖下水。對象是發包的承辦人（推論）。句子短，適合名片和車尾。</p></div>
<div class="sl"><div class="pull">淤泥要灌水才崧，報告不灌水才淳。</div><p class="note" style="margin:0">崧、淳拆開的版本。「灌水」轉兩個意思：前面是真的沖水，淤泥才鬆；後面是數字不灌水，報告才純。崧念鬆、淳念純，兩句句尾合起來就是崧淳。要念出聲才聽得出諧音，印出來第一次看可能會卡一下。</p></div>
<p class="note">從 30 句中選出。篩選只做過內部一輪；上網查重有做，但範圍有限；還沒有給外部的人試聽。</p>
''')

# 18 logo 原則
page(f'''
<div class="part">十一　標誌與標準字的設計原則</div>
<h2>主色定了以後，標誌照這幾條做</h2>
<p class="lead">這一頁是從國內外的研究、設計大師作品與企業手冊整理的原則。不是標誌設計稿。</p>
<ol>
<li><b>圖形要跟公司名一起出現。</b>新品牌還沒人認得，單獨一個圖形記不住；圖加名字比只有其中一樣好（Bresciani 與 Del Ponte，2017）。</li>
<li><b>要不要畫出行業，看客人認不認得你。</b>讓人一看就知道賣什麼的標誌，對陌生品牌較有利（Luffarelli 等，2019）。但同一研究也發現，行業本身讓人聯想到不舒服的東西時，畫出來反而扣分。清淤可能讓人想到污泥（推論：研究沒有測過清淤業），所以「做什麼」可以交給字（例如「下水道清淤・CCTV 檢視」），圖形不一定要畫管子和水滴。</li>
<li><b>一個標誌只用一個構成想法。</b>1960 到 80 年代的經典標誌 38 個裡有 33 個如此；台日公部門標誌也多半如此。</li>
<li><b>避免太細的線和縫。</b>比標誌寬度 1/14 還細的線或縫，縮到網站小圖示（約 16 像素）時會消失；名片、車門這種尺寸還沒有測過。</li>
<li><b>中文標準字要逐字調。</b>直接打字型會有字重、字寬不一的問題。「崧」是上下結構、「淳」是左右結構，並排時重心與寬度不同，要個別修。字形要原創或有授權，不直接用電腦字型當標準字。</li>
<li><b>不建議用 AI 生成標誌。</b>AI 圖形難以逐筆修改，著作權歸屬也還有爭議，容易跟現有圖形相似（推論）。</li>
</ol>
<div class="box">台灣 21 家同業裡，畫水滴水波、管子的有 8 家（第 4 頁）。崧淳若也這樣畫，會跟同業擠在一起。</div>
''')

# 19 待決定
page(f'''
<div class="part">十二　接下來</div>
<h2>要請業主決定與提供的事</h2>
<table>
<tr><th style="width:8mm">#</th><th>事項</th><th>選項或需要的東西</th><th>影響</th></tr>
<tr><td>1</td><td><b>主色</b></td><td>A 深青 #0C424A　或　B 靛藍 #333D66</td><td>決定後才能做標誌、名片、招牌</td></tr>
<tr><td>2</td><td>宣傳語</td><td>第 17 頁四句選一句，或都不要</td><td>可以晚一點決定</td></tr>
<tr><td>3</td><td>實際工程資料</td><td>作業照片、CCTV 畫面截圖、合作過的單位類型</td><td>宣傳語與公司介紹要用真實內容，不用套話</td></tr>
<tr><td>4</td><td>既有草稿</td><td>是否已有標誌、字樣、名片</td><td>有的話要先看，避免重做</td></tr>
<tr><td>5</td><td>色票打樣</td><td>選定主色後，拿 Pantone 色票與車身烤漆實物比對</td><td>螢幕色跟印刷、烤漆一定有落差</td></tr>
</table>
<h3>兩個候選各自的取捨（只列事實）</h3>
<div class="g2">
<div class="box" style="border-top:4pt solid #0C424A"><b>A 深青</b><ul style="margin-top:1.5mm">
<li>台灣同業最像的是華通衛生行的次要字樣色（9.3）；主標誌最近的是大亞（14.0）。</li>
<li>國外大品牌附近是空的（最近 16.7）。</li>
<li>偏綠的青，跟「水」的聯想比藍弱一些（推論）。</li></ul></div>
<div class="box" style="border-top:4pt solid #333D66"><b>B 靛藍</b><ul style="margin-top:1.5mm">
<li>落在台灣同業最多的藍色區；跟大亞差 7.0、一元 10.1。</li>
<li>國外跟 Insituform 差 6.7。</li>
<li>比國外同業主色都灰；觀感偏沉穩（主觀）。跟多數公家單位一樣屬藍色（推論）。</li></ul></div>
</div>
<p class="note">負責人命格條件（占三成）偏暖色，跟「主色冷色系」相反；依業主要求，以冷色系為優先。</p>
''')

# 20 附錄
page(f'''
<div class="part">附錄</div>
<h2>方法、限制與出處</h2>
<h3>怎麼量的</h3>
<ul>
<li>色差用 CIEDE2000，亮度比用 WCAG 2，都用同一支程式算，數字可重算。</li>
<li>標誌與車身顏色從圖片量：去背後統計面積，取主要顏色。照片受光線、壓縮影響，誤差可能有數個色差單位。</li>
<li>CMYK 用 Ghostscript 的一般印刷描述檔換算；Pantone 用公開的 Pantone Coated 色表（npm pantonr 0.1.0）、RAL 用 RAL Classic 色表（npm ral-colors 1.0.1）找最近一號。都不是官方色票。</li>
<li>Munsell、色彩模型與研究文獻的計算資料可以另外提供。</li>
</ul>
<h3>這份報告的範圍與限制</h3>
<ul>
<li>台灣同業 21 家、國外 48 家，取自公開網頁、商標資料與業主提供的資料夾，不是全部同業。</li>
<li>這次也上網查了崧淳本身、台灣下水道 CCTV 與清淤業者、近年水務與營造業的品牌改版：沒有找到崧淳的公開資料（新設立）；找到的改版案例（例如德國營造 Diker Bau 用青綠配紅，weandthecolor.com 報導）沒有改變本報告的結論。</li>
<li>候選色只在螢幕上比較過，還沒有實體打樣。</li>
<li>宣傳語沒有做過外部試聽。</li>
</ul>
<h3>照片出處</h3>
<ul class="note">
<li>崧淳車隊：業主提供。台灣同業：業主電腦同業資料夾、10 月 13 日台灣同業補充報告。</li>
<li>維基共享資源：台電、中華電信（Solomon203，CC BY-SA 3.0）；東京都水道局（Ypy31，CC0）。</li>
<li>國外同業：Biffa、Kanal-Türpe、Lanes Group、Thames Water、Roto-Rooter、Kier、REMONDIS、Tideway、メタウォーター、Murphy、Rioned 官網或新聞稿。手冊頁：Veolia 品牌手冊、NASA Graphics Standards Manual（1975）、U.S. EPA Graphic Standards System（1977）。著作權屬原權利人，本報告只作內部比較。</li>
<li>招牌示意圖：AI 生成空白場景，色塊以程式貼上。</li>
</ul>
''')
