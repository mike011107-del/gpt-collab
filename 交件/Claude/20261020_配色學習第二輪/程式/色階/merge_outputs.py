"""把 facts.json（步驟3）、scale_curves.json、uicp_presets.json 併進 scales.json，方便報告一次讀。"""
import json
P = '/tmp/claude-0/r2/scales/'
s = json.load(open(P + 'scales.json'))
s['崧淳候選色_只列事實'] = json.load(open(P + 'facts.json'))
s['各系統明度曲線'] = json.load(open(P + 'scale_curves.json'))
s['UI_Color_Palette_刻度預設_外掛作者近似值'] = json.load(open(P + 'uicp_presets.json'))
s['來源提交'] = {'radix-ui/colors': 'dbdb854', 'radix-ui/website': '402e749', 'material-color-utilities': 'dd62982',
               'adobe/leonardo': 'eb6481d', 'colorjs.io': '0.5.2', 'tailwindcss': '3.4.17', 'ui-ui-color-palette': 'c212430'}
json.dump(s, open(P + 'scales.json', 'w'), ensure_ascii=False, indent=1)
print(list(s.keys()))
