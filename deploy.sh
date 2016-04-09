#!/bin/bash

# Ensure that you have rebuilt the site and commited your changes

python fbscrapper.py
mv output ../output
git checkout gh-pages
mv ../output/* ./
rm -rf output
git add *
git commit -m "Build"
git push origin -f gh-pages
git checkout master
