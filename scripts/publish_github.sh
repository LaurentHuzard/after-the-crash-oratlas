#!/usr/bin/env bash
set -euo pipefail

OWNER="${GITHUB_OWNER:-LaurentHuzard}"
REPO="${GITHUB_REPO:-after-the-crash-oratlas}"
RELEASE_TAG="${RELEASE_TAG:-v0.1.0}"
REMOTE_URL="https://github.com/${OWNER}/${REPO}.git"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

command -v gh >/dev/null 2>&1 || {
  echo "GitHub CLI (gh) is required: https://cli.github.com/"
  exit 1
}

gh auth status --hostname github.com >/dev/null
python3 scripts/validate_repository.py

if [[ ! -d .git ]]; then
  git init -b main
fi

if [[ -z "$(git config user.name || true)" ]]; then
  git config user.name "Laurent Huzard"
fi
if [[ -z "$(git config user.email || true)" ]]; then
  git config user.email "26943296+LaurentHuzard@users.noreply.github.com"
fi

if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "Using existing repository $OWNER/$REPO"
else
  gh repo create "$OWNER/$REPO" \
    --public \
    --description "Substance-specific ORAtlas evidence map of amphetamine and methamphetamine withdrawal."
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Seed ORAtlas amphetamine withdrawal evidence map"
fi

git branch -M main
git push -u origin main

if gh release view "$RELEASE_TAG" --repo "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "Release $RELEASE_TAG already exists."
else
  gh release create "$RELEASE_TAG" \
    --repo "$OWNER/$REPO" \
    --target main \
    --title "After the Crash $RELEASE_TAG" \
    --notes "AI-assisted ORAtlas pilot. Human scientific review pending. Not medical advice."
fi

echo
echo "Published: https://github.com/$OWNER/$REPO"
echo "Release: https://github.com/$OWNER/$REPO/releases/tag/$RELEASE_TAG"
echo "Next: inspect the exact release in ORAtlas."
