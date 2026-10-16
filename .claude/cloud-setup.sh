#!/bin/bash
# 崧淳 gpt-collab 雲端環境安裝腳本：由梁特助貼到雲端環境設定（工作階段標題列的環境選單 → Edit → Setup script）
# 裝兩樣：1) coloraide：獨立的色彩函式庫，用來交叉驗算 colour-tool
#         2) Noto Sans TC：跟 GPT 排版稿同名的字型，算圖時字形才一致
# 來源都固定版本或提交；任何一步失敗就停（set -e）。
set -euo pipefail
pip install -q --disable-pip-version-check coloraide==4.1
FONT_DIR="$HOME/.local/share/fonts"
mkdir -p "$FONT_DIR"
curl -sSfL -m 300 -o "$FONT_DIR/NotoSansTC-wght.ttf" \
  "https://raw.githubusercontent.com/google/fonts/1d0e46c7933245c8180fe83e47917961c913bbdb/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf"
fc-cache -f >/dev/null
fam=$(fc-list "Noto Sans TC" family)
if [ -z "$fam" ]; then echo "setup 失敗：fontconfig 找不到 Noto Sans TC" >&2; exit 1; fi
echo "setup 完成：coloraide $(python3 -c 'import coloraide;print(coloraide.__version__)')、字型 $fam"
