#!/bin/sh
# Run in a normal terminal if this managed workspace cannot reach GitHub.
# The user explicitly requested a public repository under their own account.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export GIT_DIR="$project_root/.git-storage"
export GIT_WORK_TREE="$project_root"
repo="Mihir146/IE305_Social_Polarization_Group09"
if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "https://github.com/$repo.git"
fi
git push -u origin main
printf '%s\n' "https://github.com/$repo"
if command -v gh >/dev/null 2>&1; then
    gh repo view "$repo" --json url,visibility --jq '.url + " (" + .visibility + ")"' || true
fi
