#!/bin/bash

git add .
git status
git commit -m "Update"
cat ../.github-token
git push
