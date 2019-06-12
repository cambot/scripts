#!/bin/bash

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin $BRANCH
echo
echo "  --[ Change Log ]--"
git log --no-merges $BRANCH ..origin/$BRANCH --oneline
echo
git merge origin/$BRANCH
