#!/bin/bash
# 測這個環境連得到哪些來源。每次開工先跑一次，結果寫進筆記的「限制」。
# 用法：bash check_access.sh [另外要測的網址...]
# 輸出：每行「可連／擋」加網址。只測首頁能否連線，不代表該站內容能完整讀取。
urls=(
  https://raw.githubusercontent.com/w3c/wcag/main/README.md
  https://registry.npmjs.org/simple-icons
  https://pypi.org/simple/coloraide/
  https://www.pinterest.com/ https://i.pinimg.com/
  https://www.behance.net/ https://dribbble.com/
  https://www.underconsideration.com/brandnew/ https://www.pentagram.com/
  https://commons.wikimedia.org/ https://upload.wikimedia.org/
  https://www.veolia.com/ https://www.suez.com/ https://www.republicservices.com/
  https://www.lanesgroup.com/ https://www.rotorooter.com/ https://www.kanseikogyo.co.jp/
  "$@"
)
for u in "${urls[@]}"; do
  code=$(curl -sS -o /dev/null -m 12 -w "%{http_code}" "$u" 2>/dev/null)
  if [[ "$code" =~ ^[23] ]]; then echo "可連 $code $u"; else echo "擋   ${code:-000} $u"; fi
done
