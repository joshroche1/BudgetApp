#!/bin/bash

rm -rf pyqt/__pycache__
rm -rf java-swing/target
rm -rf java-quarkus/target
rm -rf python-fastapi/webapp/__pycache__
rm -rf tmp-py/webapp/__pycache__

git add .
git status
git commit -m "Update"
cat ../.github-token
git push
