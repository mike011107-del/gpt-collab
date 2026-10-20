# 把各步結果整理成 models.json（數字全部從 data/*.json 讀，不手抄）
import json
D = '/tmp/claude-0/r2/models/data/'
ap = json.load(open(D + 'apply.json'))
va = json.load(open(D + 'validation.json'))
ex = json.load(open(D + 'extras.json'))
tb = json.load(open(D + 'term_breakdown.json'))

models = [
    dict(id='ou2004_warm_cool', name='Ou 等人 2004 單色冷暖', status='已用',
         formula='WC = -0.5 + 0.02 × C*^1.07 × cos(h − 50°)（CIELAB D65，h 為色相角）；>0 偏暖、<0 偏冷',
         source='google/material-color-utilities 提交 dd62982dfdefdfc9232ce8d76e122fb1c6d188ae，typescript/temperature/temperature_cache.ts rawTemperature（註明 Ou, Woodcock and Wright 演算法）',
         grade_code='原文已讀', grade_paper='只讀到摘要或轉述（Ou 原文未取得）',
         subjects_conditions='原文未取得，受試者與實驗條件未讀到',
         validation=va['mcu_rawTemperature']),
    dict(id='ou2004_heavy_light_active_passive', name='Ou 等人 2004 輕重、主動被動', status='未取得',
         note='本機各 repo、npm 搜尋、PyPI 套件名都找不到公式；lit 串上網也查不到。不從記憶補。'),
    dict(id='ou_luo2006_harmony', name='Ou 與 Luo 2006 兩色和諧', status='未取得',
         note='同上。只知道有彩度差、明度和、明度差、色相效應四項（lit 串，只讀到轉述），沒有係數。'),
    dict(id='colorgorical', name='Colorgorical 配色評分（Gramazio、Laidlaw、Schloss 2017）', status='已用',
         source='connorgr/colorgorical 提交 90649656a57ce9743b00390473adce51a821cadc（2016-10-14）：src/model/c/scores/pairPreference.c、nameDifference.c、nameUniqueness.c、ciede2000.c、src/model/c/numpyColorgorical.c（懲罰）、src/model/model.py；論文 src/public/static/pdf/colorgorical.pdf',
         grade='原文已讀（程式與 repo 內論文 PDF）',
         scores=dict(
             perceptual_distance='CIEDE2000',
             name_difference='Heer & Stone 2012 色名分布的 Hellinger 距離，153 個英文色名（xkcd 群眾資料）；0＝名字分布相同，1＝完全不重疊',
             name_uniqueness='色名分布的熵 ÷ 4.5（程式回傳值）；論文說：名字越分散分數越高',
             pair_preference='PP = 47.6133·norm(|ΔL|) − 46.4222·norm(|ΔH|) + 75.1481·norm(κ1+κ2)，L、H 在 C 光源 CIELAB；κ＝冷度（Munsell 10R 起算的色相步數，Colorgorical 線性內插）；norm 用程式內上下限',
             penalty='Lab 色相 70–115：L≤75 乘 0.8、L>75 乘 0.85；色相 115–138 且 L≤45 乘 0.75（作者手訂，產生調色盤時用）'),
         subjects_conditions='PP 來自 Schloss & Palmer 2011：柏克萊 48 人（男女各 24），32 個彩色、992 組圖底配對（小方塊在大方塊中），螢幕、灰背景，評「多喜歡這個組合」。Colorgorical 把原本 Munsell 迴歸改成 CIE LCh，解釋 51.8% 變異（原 Munsell 版 53.5%）。白、灰、黑配對用 Colorgorical 自己的重心內插表（原實驗沒有無彩色）。Colorgorical 自己的實驗：Amazon Mechanical Turk，每種色數 20 人。',
         validation=dict(de_bounds=va['colorgorical_de_bounds'], pp_bounds=va['colorgorical_pp_bounds'],
                         nu_entropy=va['colorgorical_nu_entropy']),
         code_notes=['程式的色相差直接相減取絕對值，沒有取 360 補角；正規化上限卻是 179.27。跨 0° 的配對（藍紫配紅橘黃）分數會更低。我兩種都算。',
                     'model.py 寫的 PP 正規化上下限 107.909／−101.423，用 repo 現有查表重現不了（我算 125.97／−96.04）。所以只比相對位置，不用 0–1 分數下結論。',
                     '所有查表要先把顏色放到 5 單位格點，本次最遠移動 3.49（工程黃）。']),
    dict(id='mcu_dislike', name='Material Color Utilities 不喜歡色判斷', status='已用',
         formula='HCT 色相 90–111 且 彩度 >16 且 tone <65 → 判為不喜歡（暗黃綠）',
         source='google/material-color-utilities 提交 dd62982d，typescript/dislike/dislike_analyzer.ts（註明依 Palmer & Schloss 2010）',
         grade='原文已讀（程式）', validation=va['mcu_dislike']),
    dict(id='palettailor', name='Palettailor', status='讀過，不適用',
         source='Palettailor/Palettailor 提交 ca7d9213d24dc57835ef7f124405808cadbff00d，js/optimizeFunc.js evaluatePalette',
         note='評分只有類別分辨度、色名差、與背景的最小色差，沒有偏好或和諧分數。'),
    dict(id='schloss_palmer_2011_harmony', name='Schloss & Palmer 2011 和諧迴歸', status='只有因子，沒有係數',
         source='/tmp/claude-0/r2/lit/txt/Schloss_2011.txt（lit 串取得的原文文字）p.553 附近',
         note='較和諧的配對：色相較近、較冷、較不鮮、冷度較接近（67.3%）。文字沒有給係數，不能算。'),
]

out = dict(
    date='2026-10-19', thread='models', seed=ap['seed'],
    models=models,
    single=dict(targets=ap['targets_single'], peer_main_stats=ap['peer_main_stats'], peer_allcol_stats=ap['peer_allcol_stats'],
                peer_counts=ap['peer_counts'], targets_pct_in_peer_main=ap['targets_pct_in_peer_main'],
                random_single_stats=ap['random_single_stats'], extras=ex),
    pair=dict(targets=ap['targets_pair'], percentiles=ap['targets_pair_percentiles'], baselines=ap['baseline_pair_stats'],
              hue_wrap_share=ap['hue_wrap_share'], random_corr=ap['random_corr'], term_breakdown=tb,
              peer_pairs=ap['peer_pairs'], peer_main_x_white=ap['peer_main_x_white']),
    figures_data=['data/fig_single_wc_L.json', 'data/fig_pair_dL_pp.json', 'data/fig_coolness_curve.json', 'data/fig_ou_wc_curve.json'],
)
json.dump(out, open('/tmp/claude-0/r2/models/models.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(json.dumps(out)))
