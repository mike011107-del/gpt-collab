# PCCS 公式兩種寫法對 pccs 0.2a3 套件 doctest（套件會把結果對齊到 0.5）
import sys, math, json
sys.path.insert(0, '/tmp/claude-0/r2/theory')
from systems_lib import pccs_to_munsellH_V_C, munsell_to_pccs, pccs_tone, pccs_tone_buggy
from munsell_conv import spec_to_linear, hue_name
r05 = lambda v: round(v * 2) / 2
out = {}
for var in ('as_written', 'fixed'):
    rows = []
    for spec, expect in (((12.0, 5.5, 9.0), '3G 5.5/12'), ((2.0, 8.5, 2.0), '3.5R 8.5/2')):
        H, V, C = pccs_to_munsellH_V_C(*spec, variant=var)
        rows.append({'pccs': spec, 'expect': expect, 'got_H': hue_name(r05(H)), 'got_C_raw': round(C, 2), 'got_C_r05': r05(C)})
    for mspec, expect in (((3.0, 5.5, 12.0, 3.0), (12.0, 5.5, 9.0)), ((3.5, 8.5, 2.0, 7.0), (2.0, 8.5, 2.0))):
        H = spec_to_linear(mspec[0], mspec[3])
        p = munsell_to_pccs(H, mspec[1], mspec[2], variant=var)
        rows.append({'munsell': mspec, 'expect_pccs': expect, 'got': [round(p['h'], 2), p['l'], round(p['s'], 2)], 'tone': p['tone']})
    out[var] = rows
out['tone_doctest'] = {'(12,5.5,9)': [pccs_tone(12, 5.5, 9), pccs_tone_buggy(12, 5.5, 9)], '(2,8.5,2)': [pccs_tone(2, 8.5, 2), pccs_tone_buggy(2, 8.5, 2)], 'expect': ['v', 'p']}
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open('/tmp/claude-0/r2/theory/pccs_check.json', 'w'), ensure_ascii=False, indent=1)
