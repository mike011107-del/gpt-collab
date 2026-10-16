#!/bin/bash
# 列出 origin 上每個分支：比 main 多幾個提交、最後提交時間與訊息。
# 用途：宣稱「對方已交 X」或「X 不存在」之前，先確認所有分支；推送前確認自己的分支狀態。
# 用法：在專案庫根目錄執行 bash branch_status.sh
set -e
git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'
for b in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v '^origin/HEAD$' | grep -v '^origin$'); do
  ahead=$(git rev-list --count origin/main.."$b")
  last=$(git log -1 --format='%cs %h %<(40,trunc)%s' "$b")
  printf '%-48s 領先main %3s  %s\n' "${b#origin/}" "$ahead" "$last"
done
