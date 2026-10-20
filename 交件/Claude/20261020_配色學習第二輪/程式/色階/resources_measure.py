"""盤點時順手量的數字：
1. anthropics/skills theme-factory 10 組主題（themes/*.md）：最深對最淺的 WCAG 對比、L* 範圍。
2. knowledge-work-plugins data-visualization 的 PALETTE_CATEGORICAL（標為色弱友善）：
   兩兩最小 ΔE2000，一般與紅綠色弱（Machado 2009 deutan/protan）下；基準＝隨機 6 色組 2000 組。
3. brand-guidelines（Anthropic 品牌色）主色在淺底上的對比。
輸出 /tmp/claude-0/r2/scales/resources_measure.json
"""
import glob, itertools, json, random, re, sys
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as T

THEMES = '/tmp/claude-0/src/anthropics-skills/skills/theme-factory/themes/*.md'
DV = '/tmp/claude-0/r2/src/kwp/repo/data/skills/data-visualization/SKILL.md'


def min_de(cols, kind=None):
    cc = [T.cvd(c, kind) if kind else c for c in cols]
    return min(T.de(a, b) for a, b in itertools.combinations(cc, 2))


def main():
    out = {}
    themes = []
    for f in sorted(glob.glob(THEMES)):
        txt = open(f, encoding='utf-8').read()
        cols = re.findall(r'\*\*([^*]+)\*\*: `(#[0-9a-fA-F]{6})`', txt)
        hexes = [h for _, h in cols]
        Ls = [T.lab(h)[0] for h in hexes]
        dark = hexes[Ls.index(min(Ls))]; light = hexes[Ls.index(max(Ls))]
        themes.append({'theme': f.split('/')[-1][:-3], 'colours': cols,
                       'darkest': dark, 'lightest': light,
                       'wcag_darkest_vs_lightest': round(T.contrast(dark, light), 2),
                       'L_range': round(max(Ls) - min(Ls), 1)})
    out['theme_factory'] = {'themes': themes,
                            'n_ge_4_5': sum(1 for t in themes if t['wcag_darkest_vs_lightest'] >= 4.5),
                            'n_ge_7': sum(1 for t in themes if t['wcag_darkest_vs_lightest'] >= 7)}
    txt = open(DV, encoding='utf-8').read()
    pal = re.findall(r"#[0-9A-Fa-f]{6}", re.search(r"PALETTE_CATEGORICAL = \[(.*?)\]", txt).group(1))
    rnd = random.Random(2026)
    base = {'normal': [], 'deutan': [], 'protan': []}
    for _ in range(2000):
        s = ['#%02x%02x%02x' % tuple(rnd.randrange(256) for _ in range(3)) for _ in range(len(pal))]
        base['normal'].append(min_de(s)); base['deutan'].append(min_de(s, 'deutan')); base['protan'].append(min_de(s, 'protan'))
    pct = lambda v, x: round(100 * sum(1 for y in v if y < x) / len(v), 1)
    dv = {}
    for k in ('normal', 'deutan', 'protan'):
        x = min_de(pal, None if k == 'normal' else k)
        dv[k] = {'min_dE2000': round(x, 2), 'random_median': round(sorted(base[k])[1000], 2), 'percentile_vs_random': pct(base[k], x)}
    worst = min(itertools.combinations(pal, 2), key=lambda p: T.de(T.cvd(p[0], 'deutan'), T.cvd(p[1], 'deutan')))
    out['kwp_dataviz_palette'] = {'palette': pal, 'stats': dv, 'closest_pair_deutan': list(worst)}
    out['brand_guidelines'] = {
        'orange_on_light': round(T.contrast('#d97757', '#faf9f5'), 2),
        'blue_on_light': round(T.contrast('#6a9bcc', '#faf9f5'), 2),
        'green_on_light': round(T.contrast('#788c5d', '#faf9f5'), 2),
        'dark_on_light': round(T.contrast('#141413', '#faf9f5'), 2)}
    json.dump(out, open('/tmp/claude-0/r2/scales/resources_measure.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({'tf': [(t['theme'], t['wcag_darkest_vs_lightest'], t['L_range']) for t in themes],
                      'tf_n': (out['theme_factory']['n_ge_4_5'], out['theme_factory']['n_ge_7']),
                      'dv': out['kwp_dataviz_palette'], 'bg': out['brand_guidelines']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
