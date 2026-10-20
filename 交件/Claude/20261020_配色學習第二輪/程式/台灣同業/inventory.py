# 盤點：主 PDF 25 家＋資料夾 14 家，哪些拿得到 logo 圖、哪個版本
import json
W='/tmp/claude-0/r2/tw/'
TW={t['company']:t for t in json.load(open(W+'tw_peers.json'))}
pdf25=['全基','銘源','升野','積德','力士通','華通衛生行','九升','宏隆','浩源','晨佳','久大','派浦崴洱','力賀','昭揚','浚富','瑞碁','龍祥','三福','程堡','廣村','盛泰','鼎宸','辰福','鎮海','順捷']
folder14=['華通','銘源','邦盛','天福','大亞','久大','源昌','森淨家','逸居管必潔','綠邑','日技','宏隆','康立','一元']
alias={'華通衛生行':'華通'}
rows=[]
for nm in dict.fromkeys(pdf25+folder14):
    key=alias.get(nm,nm); t=TW.get(key)
    rows.append(dict(company=nm,in_pdf25=nm in pdf25,in_folder14=nm in folder14,
        has_image=t is not None,tier=t['tier'] if t else None,versions=([t['vid']]+t['alt']) if t else [],
        status=('原文已讀（圖檔已開）' if t else '未取得'),
        note=('補充 PDF：華通清淤品牌與華通衛生行主體的對應待確認' if nm in('華通衛生行','華通') else
              '首頁找不到 logo，只有網站文字與網站色（補充 PDF 與同業色彩整理.md 都這樣寫）' if nm=='銘源' else
              '補充 PDF 寫未找到可靠 logo' if not t else '')))
have=sorted({alias.get(r['company'],r['company']) for r in rows if r['has_image']})
out=dict(說明='主 PDF＝Taiwan_Sewer_CCTV_Competitor_Intelligence_With_Logo_CIS_20261013.pdf p5（01–13）、p6（14–25）登記總表；有圖 11／未取得 14 的分法出自補充 PDF 首頁（主 PDF p28 附錄同一頁）；資料夾＝崧淳同業logo/（同業色彩整理.md 的 14 家，銘源沒有 logo 圖，有圖 13 家）',
  有圖公司數=len(have),有圖公司=have,主PDF有圖=sum(r['has_image'] for r in rows if r['in_pdf25']),主PDF未取得=[r['company'] for r in rows if r['in_pdf25'] and not r['has_image']],
  版本數=sum(len(r['versions']) for r in rows if r['company']!='華通衛生行'),rows=rows)
json.dump(out,open(W+'data/inventory.json','w'),ensure_ascii=False,indent=1)
print(out['有圖公司數'],out['主PDF有圖'],len(out['主PDF未取得']),out['主PDF未取得'],out['版本數'])
