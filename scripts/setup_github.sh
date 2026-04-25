#!/usr/bin/env bash
set -e

REPO_NAME="${REPO_NAME:-qr-generator-bot}"
GITHUB_USER="${GITHUB_USER:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

if [[ -z "$GITHUB_TOKEN" || -z "$GITHUB_USER" ]]; then
    echo "ERROR: Set GITHUB_TOKEN and GITHUB_USER environment variables."
    exit 1
fi

echo "Creating GitHub repository $REPO_NAME for user $GITHUB_USER..."

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"$REPO_NAME\",\"private\":false,\"description\":\"Premium QR generator bot on aiogram 3\"}")

if [[ "$HTTP_CODE" == "201" ]]; then
    echo "Repo created."
elif [[ "$HTTP_CODE" == "422" ]]; then
    echo "Repo already exists."
else
    echo "Failed (HTTP $HTTP_CODE). Check token/permissions."
    exit 1
fi

git remote remove origin 2>/dev/null || true
git remote add origin "https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
git branch -M main
git push -u origin main

echo "Done. Visit https://github.com/$GITHUB_USER/$REPO_NAME"
