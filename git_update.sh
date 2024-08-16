#!/bin/bash

rm -rf pyqt/__pycache__
rm -rf java-temp/target
rm -rf java-quarkus/target
rm -rf python-fastapi/webapp/__pycache__
rm python-fastapi/upload/*

git add .
git status
git commit -m "Update"
cat ../.github-token
git push
