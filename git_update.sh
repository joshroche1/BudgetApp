#!/bin/bash

rm -rf java-temp/target
rm -rf java-quarkus/target
rm -rf python-fastapi/webapp/__pycache__

git add .
git status
git commit -m "Update"
cat ../.github-token
git push
