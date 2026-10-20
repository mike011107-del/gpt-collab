"""核對原文的數字說法。
1. MCU concepts/color_terms.md：tone 差 40 保證 WCAG ≥3.0；差 50 保證 ≥4.5。
   方法：tone 0..100 每 0.1 一格，所有差≥40（或≥50）的配對，找最小對比。
"""
import sys
sys.path.insert(0, '/tmp/claude-0/r2/scales')
import hct as H
def cr(t1, t2):
    y1, y2 = H.y_from_lstar(t1), H.y_from_lstar(t2)
    hi, lo = max(y1, y2), min(y1, y2)
    return (hi + 5) / (lo + 5)
for d in (40, 50):
    worst = min((cr(t / 10, t / 10 + d), t / 10) for t in range(0, int((100 - d) * 10) + 1))
    print('tone diff', d, 'min WCAG', round(worst[0], 3), 'at tones', worst[1], worst[1] + d)
