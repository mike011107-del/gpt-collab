# pro-color-harmonies（commit 09f8da8）src/utils/color.ts 第 41–47 行的「泥濁區」只看 OKLCH 色相：25–65 褐橄欖、100–140 病綠、180–200 屍青
# 檢查：崧淳三色與 48 家同業彩色有幾個落在裡面
import sys, json
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as ct
Z = [(25, 65, 'brown-olive'), (100, 140, 'sick-green'), (180, 200, 'corpse-cyan')]
def zone(hx):
    L, C, h = ct.oklch(hx)
    if C < 0.04: return None, round(h, 1), round(C, 3)
    for a, b, n in Z:
        if a <= h <= b: return n, round(h, 1), round(C, 3)
    return None, round(h, 1), round(C, 3)
peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
hits = [{'peer': p['name'], 'hex': c, 'zone': zone(c)[0], 'okh': zone(c)[1], 'okC': zone(c)[2]} for p in peers for c in p['cols'] if zone(c)[0]]
n_all = sum(1 for p in peers for c in p['cols'] if ct.oklch(c)[1] >= 0.04)
out = {'songchun': {k: dict(zip(['zone', 'okh', 'okC'], zone(v))) for k, v in {'深青': '#0C424A', '靛藍': '#333D66', '工程黃': '#D68702'}.items()},
       'peer_hits': hits, 'n_peer_chromatic': n_all, 'zone_share_of_hue_circle': round((40 + 40 + 20) / 360, 3)}
json.dump(out, open('/tmp/claude-0/r2/theory/muddy_check.json', 'w'), ensure_ascii=False, indent=1)
print(out['songchun']); print(len(hits), n_all); print([(h['peer'], h['hex'], h['zone'], h['okh']) for h in hits])
