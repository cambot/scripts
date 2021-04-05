#!/bin/bash

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin $BRANCH
git fetch origin --prune
echo
echo "  --[ Change Log ]--"
git log --no-merges $BRANCH ..origin/$BRANCH --oneline
echo
git merge origin/$BRANCH
exit 0
