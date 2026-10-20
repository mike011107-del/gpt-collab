"""步驟3：深青、靛藍、工程黃在 HCT、Radix、Material tonal palette 的位置（只列事實）。
另算基準：隨機 sRGB 色、48 家同業 logo 色，各自離 Radix 最近一階的色差分布，與 HCT 分布。
輸出 /tmp/claude-0/r2/scales/facts.json
"""
import json, math, random, sys
sys.path.insert(0, '/tmp/claude-0/r2/scales')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import hct as H
import radix_gen as R
import colourtool as T

TARGETS = {'深青': '#0C424A', '靛藍': '#333D66', '工程黃': '#D68702'}
STEP_USE = {1: '頁面底色', 2: '次要底色', 3: '元件底色（平常）', 4: '元件底色（滑過）', 5: '元件底色（按下、選取）',
            6: '不可互動的細框線', 7: '可互動元件框線', 8: '較強框線、焦點環', 9: '實色底（最純的一階）',
            10: '實色底滑過', 11: '低對比文字', 12: '高對比文字'}
M3_ROLES_LIGHT = {100: 'onPrimary（主色上的字）、surfaceContainerLowest', 90: 'primaryContainer（主色淡底）',
                  80: 'inversePrimary', 40: 'primary（主色）', 30: 'onPrimaryContainer（淡底上的字）',
                  98: 'surface／background（中性色板）', 10: 'onSurface（中性色板的字）'}
M3_ROLES_DARK = {80: 'primary', 20: 'onPrimary', 30: 'primaryContainer', 90: 'onPrimaryContainer', 40: 'inversePrimary',
                 6: 'surface／background（中性色板）'}

ALL = {n: R.HEX[n] for n in R.ALL_HEX_NAMES}


def nearest_radix(hx, k=3):
    rows = []
    for n, sc in ALL.items():
        for i, s in enumerate(sc):
            rows.append((T.de(hx, s), n, i + 1, s))
    rows.sort()
    return rows[:k]


def max_chroma(h, t):
    hx = H.hct_to_hex(h, 200, t)
    return H.hct_from_hex(hx)[1]


def pct(vals, v):
    return round(100 * sum(1 for x in vals if x < v) / len(vals), 1)


def main():
    out = {'targets': {}, 'baseline': {}}
    # 基準 1：隨機 sRGB 色（固定種子 2026）
    rnd = random.Random(2026)
    rand = ['#%02x%02x%02x' % (rnd.randrange(256), rnd.randrange(256), rnd.randrange(256)) for _ in range(2000)]
    rand_near = [nearest_radix(c, 1)[0][0] for c in rand]
    # 基準 2：48 家同業 logo 彩色
    peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
    pcols = [(p['name'], c) for p in peers for c in p['cols']]
    peer_near = [nearest_radix(c, 1)[0] for _, c in pcols]
    peer_de = [x[0] for x in peer_near]
    peer_hct = [H.hct_from_hex(c) for _, c in pcols]
    # 隨機色的 HCT 相對彩度（chroma / 同色相同明度最大 chroma）
    def rel_chroma(hx):
        h, c, t = H.hct_from_hex(hx)
        if t < 1 or t > 99 or c < 1:
            return 0.0
        return c / max_chroma(h, t)
    rand_rel = [rel_chroma(c) for c in rand[:400]]
    peer_rel = [rel_chroma(c) for _, c in pcols]
    sm = lambda v: sorted(v)[len(v) // 2]
    out['baseline'] = {
        'random_srgb_n': len(rand), 'random_seed': 2026,
        'random_nearest_radix_dE2000_median': round(sm(rand_near), 2),
        'random_nearest_radix_dE2000_p10_p90': [round(sorted(rand_near)[len(rand_near) // 10], 2),
                                                round(sorted(rand_near)[len(rand_near) * 9 // 10], 2)],
        'peer_colours_n': len(pcols),
        'peer_nearest_radix_dE2000_median': round(sm(peer_de), 2),
        'peer_nearest_radix_step_counts': {str(s): sum(1 for x in peer_near if x[2] == s) for s in range(1, 13)},
        'peer_hct_tone_median': round(sm([x[2] for x in peer_hct]), 1),
        'peer_hct_chroma_median': round(sm([x[1] for x in peer_hct]), 1),
        'random_rel_chroma_median_n400': round(sm(rand_rel), 3),
        'peer_rel_chroma_median': round(sm(peer_rel), 3),
    }
    for name, hx in TARGETS.items():
        h, c, t = H.hct_from_hex(hx)
        mc = max_chroma(h, t)
        near = nearest_radix(hx, 3)
        # Radix 產生器自己用的配對（OKLab 距離）
        src = R.oklch_from_hex(hx)
        bg = R.oklch_from_hex('#FFFFFF')
        _, info = R.get_scale_from_color(src, R.LIGHT, bg)
        acc0 = R.get_scale_from_color(src, R.LIGHT, bg)[0][0]
        used_as_9 = R.deltaEOK(src, acc0) * 100 >= 25
        txt = R.to_hex(R.get_text_color(src))
        # Material：本身 tone、標準 13 階中最近的兩階、Tonal Spot 會把 chroma 改成 36
        std = H.TONES
        lower = max(x for x in std if x <= t); upper = min(x for x in std if x >= t)
        disliked = (90 <= round(h) <= 111) and round(c) > 16 and round(t) < 65
        rec = {
            'hex': hx,
            'hct': {'hue': round(h, 1), 'chroma': round(c, 1), 'tone': round(t, 1)},
            'hct_max_chroma_at_this_hue_tone': round(mc, 1),
            'chroma_share_of_max': round(c / mc, 3),
            'chroma_percentile_vs_peers': pct([x[1] for x in peer_hct], c),
            'tone_percentile_vs_peers': pct([x[2] for x in peer_hct], t),
            'oklch': [round(v, 3) for v in T.oklch(hx)],
            'radix_nearest_dE2000': [{'scale': n, 'step': s, 'hex': sh, 'dE2000': round(d, 2), 'step_use': STEP_USE[s]}
                                      for d, n, s, sh in near],
            'radix_nearest_percentile_vs_random': pct(rand_near, near[0][0]),
            'radix_nearest_percentile_vs_peers': pct(peer_de, near[0][0]),
            'radix_generator_match_oklab': {k: (round(v, 4) if isinstance(v, float) else v) for k, v in info.items()},
            'radix_generator_keeps_as_step9': used_as_9,
            'radix_generator_text_on_step9': txt,
            'material_tone': round(t, 1),
            'material_std_tones_around': [lower, upper],
            'material_roles_light_at_those_tones': {str(x): M3_ROLES_LIGHT.get(x, '') for x in (lower, upper)},
            'material_tonal_spot_primary_chroma': 36,
            'material_dislike_rule_hit': disliked,
            'wcag_vs_white': round(T.contrast(hx, '#ffffff'), 2),
        }
        out['targets'][name] = rec
    json.dump(out, open('/tmp/claude-0/r2/scales/facts.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])


if __name__ == '__main__':
    main()
