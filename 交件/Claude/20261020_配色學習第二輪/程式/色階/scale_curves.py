"""各設計系統色階的明度曲線（給報告畫圖），並核對 Radix「第 9 階彩度最高」的說法。
資料：
  Radix light.ts（radix-ui/colors dbdb854）
  Tailwind CSS 3.4.17 lib/public/colors.js（npm registry tarball）
  Material tonal palette：tone 就是 L*（MCU concepts/color_terms.md），直接列 13 階
輸出 /tmp/claude-0/r2/scales/scale_curves.json
"""
import json, re, sys
sys.path.insert(0, '/tmp/claude-0/r2/scales')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import radix_gen as R
import colourtool as T

TW = '/tmp/claude-0/r2/src/npm-tailwindcss3/package/lib/public/colors.js'


def load_tw():
    txt = open(TW, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'(\w+): \{\s*(50: "#[0-9a-f]{6}".*?)\}', txt, re.S):
        vals = re.findall(r'(\d+): "(#[0-9a-f]{6})"', m.group(2))
        if len(vals) == 11:
            out[m.group(1)] = [v for _, v in vals]
    return out


def med(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def main():
    res = {}
    chromatic = [n for n in R.ALL_HEX_NAMES if n not in R.GRAY_NAMES]
    rx = {n: [round(T.lab(h)[0], 1) for h in R.HEX[n]] for n in chromatic}
    rx_c = {n: [T.oklch(h)[1] for h in R.HEX[n]] for n in chromatic}
    peak = {n: 1 + max(range(12), key=lambda i: rx_c[n][i]) for n in chromatic}
    res['radix'] = {
        'steps': list(range(1, 13)),
        'median_L_per_step': [round(med([rx[n][i] for n in chromatic]), 1) for i in range(12)],
        'L_range_per_step': [[min(rx[n][i] for n in chromatic), max(rx[n][i] for n in chromatic)] for i in range(12)],
        'n_scales': len(chromatic),
        'peak_oklch_chroma_step_counts': {str(s): sum(1 for v in peak.values() if v == s) for s in range(1, 13)},
        'scales_where_step9_not_peak': {n: peak[n] for n in chromatic if peak[n] != 9},
        'blue_L': rx['blue'], 'amber_L': rx['amber'], 'teal_L': rx['teal'],
    }
    tw = load_tw()
    tw_chrom = {n: v for n, v in tw.items() if n not in ('slate', 'gray', 'zinc', 'neutral', 'stone')}
    twL = {n: [round(T.lab(h)[0], 1) for h in v] for n, v in tw_chrom.items()}
    twC = {n: [T.oklch(h)[1] for h in v] for n, v in tw_chrom.items()}
    twpeak = {n: [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950][max(range(11), key=lambda i: twC[n][i])] for n in tw_chrom}
    res['tailwind3'] = {
        'steps': [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950],
        'n_palettes': len(tw_chrom),
        'median_L_per_step': [round(med([twL[n][i] for n in tw_chrom]), 1) for i in range(11)],
        'L_range_per_step': [[min(twL[n][i] for n in tw_chrom), max(twL[n][i] for n in tw_chrom)] for i in range(11)],
        'peak_oklch_chroma_step_counts': {str(s): sum(1 for v in twpeak.values() if v == s) for s in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]},
        'blue_hex': tw['blue'], 'blue_L': twL['blue'], 'amber_L': twL['amber'],
    }
    res['material3'] = {'tones': [100, 99, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0],
                        'L_equals_tone': True,
                        'note': '同一色板每一階 L* 固定，不隨色相變；色相、彩度不夠時降彩度保明度。'}
    json.dump(res, open('/tmp/claude-0/r2/scales/scale_curves.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('L_range_per_step',)} for k, v in res.items()}, ensure_ascii=False)[:3000])


if __name__ == '__main__':
    main()
