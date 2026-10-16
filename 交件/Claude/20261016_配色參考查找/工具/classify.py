"""顏色分類：冷深色、工程黃、第三色家族。門檻用 OKLCH。"""
from colormath import oklch

# 工程黃：RAL 1018 #FACA30 = L0.86 C0.16 H90；Cat #FFCD11 H91；琥珀 #F3B51B H83
YELLOW = dict(h=(72, 108), L=0.72, C=0.10)
# 冷色：綠到藍（不含紫，紫色業主已排除）
COOL_H = (140, 275)


def is_yellow(h):
    L, C, H = oklch(h)
    return YELLOW['h'][0] <= H <= YELLOW['h'][1] and L >= YELLOW['L'] and C >= YELLOW['C']


def is_cool(h, maxL=0.60, minC=0.03):
    L, C, H = oklch(h)
    return COOL_H[0] <= H <= COOL_H[1] and L <= maxL and C >= minC


def cool_sub(h):
    """冷色細分：綠／青綠／青／藍／深藍。"""
    L, C, H = oklch(h)
    if H < 175: return '綠'
    if H < 200: return '青綠'
    if H < 230: return '青'
    return '藍'


def family(h):
    """第三色家族（給非冷深、非工程黃的顏色用）。"""
    L, C, H = oklch(h)
    if C < 0.035:
        if L >= 0.90: return '白／米白'
        if L >= 0.65: return '淺灰'
        if L >= 0.40: return '中灰'
        return '炭黑'
    if L >= 0.88 and C < 0.08:
        return '白／米白'
    if 72 <= H <= 108:
        return '淺黃／米黃' if L >= 0.88 else ('芥末／土黃' if L < 0.72 else '黃')
    if H < 20 or H >= 340:
        return '粉' if L >= 0.75 else '紅'
    if H < 55:
        return '珊瑚／橘紅' if L >= 0.55 else '紅褐'
    if H < 72:
        return '橘' if L >= 0.62 else '棕／赭'
    if H < 140:
        return '黃綠／橄欖'
    if H <= 275:
        sub = cool_sub(h)
        return ('淺' if L >= 0.75 else '中' if L > 0.60 else '深') + sub
    return '紫'
