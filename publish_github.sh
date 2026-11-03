#!/bin/sh
# Run in a normal terminal if this managed workspace cannot reach GitHub.
# The user explicitly requested a public repository under their own account.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export GIT_DIR="$project_root/.git-storage"
export GIT_WORK_TREE="$project_root"
owner=$(gh api user --jq .login)
repo="$owner/ie305-product-launch"
if gh repo view "$repo" --json nameWithOwner >/dev/null 2>&1; then
    if ! git remote get-url origin >/dev/null 2>&1; then
        git remote add origin "https://github.com/$repo.git"
    fi
    visibility=$(gh repo view "$repo" --json visibility --jq .visibility)
    if [ "$visibility" != PUBLIC ]; then
        gh repo edit "$repo" --visibility public --accept-visibility-change-consequences
    fi
    git push -u origin main
else
    gh repo create "$repo" --public --description 'IE305 agent-based simulation: product launch, word of mouth and sampling strategies in a synthetic campus market' --source "$project_root" --remote origin --push
fi
gh repo view "$repo" --json url,visibility --jq '.url + " (" + .visibility + ")"'
