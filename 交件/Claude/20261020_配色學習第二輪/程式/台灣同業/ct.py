# 載入 colour-tool（專案庫內、已過 selftest）的函式，避免重寫公式
import importlib.util
_p='/home/user/gpt-collab/.claude/skills/colour-tool/scripts/colourtool.py'
_s=importlib.util.spec_from_file_location('colourtool',_p); ct=importlib.util.module_from_spec(_s); _s.loader.exec_module(ct)
lab=ct.lab; oklch=ct.oklch; de=ct.de; lch=ct.lch; contrast=ct.contrast
def okh(h): return oklch(h)[2]
def hue_diff(a,b):
    d=abs(a-b)%360; return min(d,360-d)
