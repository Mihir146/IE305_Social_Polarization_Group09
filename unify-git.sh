#!/usr/bin/env bash
# One-time repair: keep all commits and make ordinary git/project-git share metadata.
# Run from a normal terminal because the managed tool cannot rename the root .git.
set -euo pipefail
project_root=$(cd -- "$(dirname -- "$0")" && pwd)
cd -- "$project_root"
if [[ ! -d .git-storage ]]; then
  echo 'No alternate metadata here; this ordinary clone needs no unification.'
  exit 0
fi
project_git() { git --git-dir="$project_root/.git-storage" --work-tree="$project_root" "$@"; }
if [[ -d .git ]]; then
  if [[ -e .git-root-backup ]]; then
    echo 'A .git-root-backup already exists. Preserve it and inspect before rerunning.' >&2
    exit 1
  fi
  if ! git diff --cached --quiet; then
    echo 'The ordinary Git index has staged edits. Commit them first so their history is preserved.' >&2
    exit 1
  fi
  project_git fetch "$project_root/.git" main:refs/remotes/workspace/main
  project_git merge --no-edit workspace/main
  project_git fetch origin main
  project_git merge --no-edit origin/main
  # Prepare the supported gitdir pointer before moving metadata. No working files are reset.
  printf 'gitdir: .git-storage\n' > .git-pointer.tmp
  mv -- .git .git-root-backup
  if ! mv -- .git-pointer.tmp .git; then
    mv -- .git-root-backup .git
    exit 1
  fi
  echo 'Unified Git metadata. Original .git retained in ignored .git-root-backup/.'
elif [[ -f .git ]] && [[ $(git rev-parse --absolute-git-dir) == "$project_root/.git-storage" ]]; then
  echo 'Git metadata is already unified.'
else
  echo 'Unexpected .git setup; no metadata was changed.' >&2
  exit 1
fi
git status --short --branch
git push origin main
