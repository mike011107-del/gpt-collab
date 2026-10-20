"""步驟4：示意例子 Vattenfall 藍 #2071B5（跟崧淳無關），照 Material、Radix、Leonardo 各展開一次。
輸出 /tmp/claude-0/r2/scales/scales.json（給報告畫圖用的色碼與數字）
"""
import json, sys
sys.path.insert(0, '/tmp/claude-0/r2/scales')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import hct as H
import radix_gen as R
import leonardo as L
import colourtool as T

EX = '#2071B5'
STEP_USE = {1: '頁面底色', 2: '次要底色', 3: '元件底色（平常）', 4: '元件底色（滑過）', 5: '元件底色（按下、選取）',
            6: '不可互動的細框線', 7: '可互動元件框線', 8: '較強框線、焦點環', 9: '實色底（最純的一階，品牌色本身）',
            10: '實色底滑過', 11: '低對比文字', 12: '高對比文字'}


def sw(hx):
    return {'hex': hx, 'L*': round(T.lab(hx)[0], 1), 'wcag_vs_white': round(T.contrast(hx, '#ffffff'), 2),
            'oklch': [round(v, 3) for v in T.oklch(hx)]}


def material():
    h, c, t = H.hct_from_hex(EX)
    tones = H.TONES
    pal = lambda hue, chroma: [dict(tone=x, **sw(H.tonal_palette(hue, chroma, [x])[x])) for x in tones]
    tonal_spot = {
        'primary': {'hue': round(h, 1), 'chroma': 36, 'tones': pal(h, 36)},
        'secondary': {'hue': round(h, 1), 'chroma': 16, 'tones': pal(h, 16)},
        'tertiary': {'hue': round((h + 60) % 360, 1), 'chroma': 24, 'tones': pal((h + 60) % 360, 24)},
        'neutral': {'hue': round(h, 1), 'chroma': 6, 'tones': pal(h, 6)},
        'neutral_variant': {'hue': round(h, 1), 'chroma': 8, 'tones': pal(h, 8)},
        'error': {'hue': 25, 'chroma': 84, 'tones': pal(25, 84)},
    }
    fidelity_primary = {'hue': round(h, 1), 'chroma': round(c, 1), 'tones': pal(h, c)}
    # 2021 規格的起始 tone（color_spec_2021.ts），未做對比微調
    roles = [
        ('primary', 'primary', 40, 80), ('onPrimary', 'primary', 100, 20),
        ('primaryContainer', 'primary', 90, 30), ('onPrimaryContainer', 'primary', 30, 90),
        ('secondary', 'secondary', 40, 80), ('secondaryContainer', 'secondary', 90, 30),
        ('tertiary', 'tertiary', 40, 80), ('tertiaryContainer', 'tertiary', 90, 30),
        ('surface', 'neutral', 98, 6), ('onSurface', 'neutral', 10, 90),
        ('surfaceVariant', 'neutral_variant', 90, 30), ('onSurfaceVariant', 'neutral_variant', 30, 80),
        ('outline', 'neutral_variant', 50, 60), ('outlineVariant', 'neutral_variant', 80, 30),
        ('error', 'error', 40, 80),
    ]
    hc = {k: (v['hue'], v['chroma']) for k, v in tonal_spot.items()}
    hc['primary'] = (h, 36); hc['secondary'] = (h, 16); hc['tertiary'] = ((h + 60) % 360, 24)
    hc['neutral'] = (h, 6); hc['neutral_variant'] = (h, 8)
    role_rows = []
    for name, p, tl, td in roles:
        hh, cc = hc[p]
        role_rows.append({'role': name, 'palette': p, 'tone_light': tl, 'hex_light': H.hct_to_hex(hh, cc, tl),
                          'tone_dark': td, 'hex_dark': H.hct_to_hex(hh, cc, td)})
    return {
        'source_hct': {'hue': round(h, 1), 'chroma': round(c, 1), 'tone': round(t, 1)},
        'note': 'Tonal Spot 是 MCU 預設變體：主色板 chroma 固定 36，不管原色多鮮；Fidelity／Content 變體才用原色 chroma，並把 primaryContainer 設成原色 tone。',
        'tonal_spot_palettes': tonal_spot,
        'fidelity_primary_palette': fidelity_primary,
        'roles_2021_start_tones': role_rows,
    }


def radix():
    g = R.generate(EX)
    acc = [dict(step=i + 1, use=STEP_USE[i + 1], **sw(x)) for i, x in enumerate(g['accent'])]
    gray = [dict(step=i + 1, **sw(x)) for i, x in enumerate(g['gray'])]
    blue = [dict(step=i + 1, **sw(x)) for i, x in enumerate(R.HEX['blue'])]
    # 文件說：第 11、12 階放在同色系第 2 階上，APCA 至少 Lc 60、Lc 90
    def apca_check(sc):
        return {'step11_on_step2_Lc': round(abs(T.apca(sc[10], sc[1])), 1),
                'step12_on_step2_Lc': round(abs(T.apca(sc[11], sc[1])), 1)}
    apca_all = {n: apca_check(R.HEX[n]) for n in R.ALL_HEX_NAMES}
    min11 = min(v['step11_on_step2_Lc'] for v in apca_all.values())
    min12 = min(v['step12_on_step2_Lc'] for v in apca_all.values())
    return {
        'generator_inputs': {'accent': EX, 'gray': '#8B8D98', 'background': '#FFFFFF', 'appearance': 'light'},
        'match': {k: (round(v, 4) if isinstance(v, float) else v) for k, v in g['match'].items()},
        'accent_scale': acc, 'text_on_step9': g['contrast_text'], 'gray_scale': gray,
        'official_blue_for_comparison': blue,
        'apca_generated': apca_check(g['accent']),
        'apca_official_min_over_all_scales': {'step11_on_step2_Lc_min': min11, 'step12_on_step2_Lc_min': min12,
                                              'scales_checked': len(apca_all)},
        'apca_official_per_scale': apca_all,
    }


def leonardo():
    targets = [round(T.contrast(x, '#ffffff'), 2) for x in R.HEX['blue']]
    lab = L.search([EX], targets, '#ffffff', 'LAB')
    rgb = L.search([EX], targets, '#ffffff', 'RGB')
    return {
        'note': '目標對比值借用 Radix 官方 blue 12 階對白底的 WCAG 對比，讓三套方法排在同一條尺上比較；色鍵只有 #2071B5 一個，白底。',
        'targets_from_radix_blue': targets,
        'lab_interpolation': [dict(**x, **{'L*': round(T.lab(x['hex'])[0], 1)}) for x in lab],
        'rgb_interpolation': [dict(**x, **{'L*': round(T.lab(x['hex'])[0], 1)}) for x in rgb],
        'key_cam02_J': round(L.cam02_J(EX), 2),
        'key_position_on_3000': round(3000 - 3000 * L.cam02_J(EX) / 100, 1),
    }


def main():
    out = {'example': {'name': 'Vattenfall 藍', 'hex': EX, **sw(EX),
                       'why': '跟崧淳無關的公用事業藍，只拿來示範方法'},
           'material': material(), 'radix': radix(), 'leonardo': leonardo()}
    # 例子本身在 Radix 生成色階、Material 色板中的位置
    out['example']['radix_step9_equals_source'] = out['radix']['accent_scale'][8]['hex'].lower() == EX.lower()
    json.dump(out, open('/tmp/claude-0/r2/scales/scales.json', 'w'), ensure_ascii=False, indent=1)
    m = out['material']; r = out['radix']; l = out['leonardo']
    print('HCT', m['source_hct'])
    print('TS primary', [x['hex'] for x in m['tonal_spot_palettes']['primary']['tones']])
    print('Fid primary', [x['hex'] for x in m['fidelity_primary_palette']['tones']])
    print('Radix', [x['hex'] for x in r['accent_scale']], r['text_on_step9'], r['match'])
    print('Radix gray', [x['hex'] for x in r['gray_scale']])
    print('APCA', r['apca_generated'], r['apca_official_min_over_all_scales'])
    print('Leo targets', l['targets_from_radix_blue'])
    print('Leo LAB', [(x['hex'], x['ratio_got']) for x in l['lab_interpolation']])
    print('Leo RGB', [x['hex'] for x in l['rgb_interpolation']])
    print('roles', [(x['role'], x['hex_light'], x['hex_dark']) for x in m['roles_2021_start_tones']][:6])


if __name__ == '__main__':
    main()
