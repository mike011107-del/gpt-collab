"""驗證 radix_gen.py：拿 Radix 自己的第 9 階當輸入，產生的 12 階應接近官方色階。"""
import sys, json
sys.path.insert(0, '/tmp/claude-0/r2/scales')
import radix_gen as R
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as T
out = {}
for name in ['blue', 'teal', 'indigo', 'amber', 'orange', 'grass', 'tomato', 'cyan', 'iris', 'jade']:
    off = R.HEX[name]
    g = R.generate(off[8])
    des = [round(T.de(a, b), 2) for a, b in zip(g['accent'], off)]
    out[name] = {'max_dE2000': max(des), 'median_dE2000': sorted(des)[6], 'match': g['match']['closest_scale'],
                 'gen': g['accent'], 'official': off}
    print(name, 'max', max(des), 'per-step', des)
json.dump(out, open('/tmp/claude-0/r2/scales/radix_validate.json', 'w'), indent=1)
