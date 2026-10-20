# 把 Colorgorical（connorgr/colorgorical，提交 90649656）C 原始碼裡的查表陣列
# 轉成 numpy 檔，給 colorgorical_port.py 用。只讀數字，不執行任何外部程式。
# 用法：python3 -I parse_colorgorical.py <repo 路徑> <輸出 npz>
import re, sys
import numpy as np

repo = sys.argv[1]
out = sys.argv[2]
C = repo + '/src/model/c/'

files = {
    'LAB': ('util/labList.c', 'COLORGORICAL_LAB', int),
    'LAB_IS_VALID_RGB': ('util/labList.c', 'COLORGORICAL_LAB_IS_VALID_RGB', int),
    'CIS': ('util/colorIndex.c', 'COLORGORICAL_CIS', int),
    'COOLNESS': ('util/labToCoolness.c', 'COLORGORICAL_LAB_TO_COOLNESS', float),
    'CH': ('util/labToCH.c', 'COLORGORICAL_LAB_TO_CH', float),
    'ACHROMPREF': ('util/labToAchromaticPreference.c', 'COLORGORICAL_LAB_TO_ACHROMATICPREF', float),
    'NAMES_CCOUNT': ('scores/colorNames/colorNames_Counts.c', 'COLORGORICAL_NAMES_CCOUNT', int),
    'NAMES_TCOUNT': ('scores/colorNames/colorNames_Counts.c', 'COLORGORICAL_NAMES_TCOUNT', int),
    'NAMES_T': ('scores/colorNames/colorNames_T.c', 'COLORGORICAL_NAMES_T', int),
}

arrays = {}
cache = {}
for key, (fn, name, typ) in files.items():
    if fn not in cache:
        cache[fn] = open(C + fn, encoding='utf-8', errors='replace').read()
    txt = cache[fn]
    m = re.search(re.escape(name) + r'\s*\[\s*\d*\s*\]\s*=\s*\{', txt)
    if not m:
        raise SystemExit('找不到 ' + name)
    start = m.end()
    end = txt.index('}', start)
    body = txt[start:end].replace('NAN', 'nan')
    arr = np.array([float(x) for x in body.split(',') if x.strip()], dtype=float)
    if typ is int:
        arr = arr.astype(np.int64)
    arrays[key] = arr
    print(key, arr.shape, arr[:6])

np.savez_compressed(out, **arrays)
print('saved', out)
