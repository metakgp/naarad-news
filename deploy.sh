#!/bin/bash

python fbscraper.py
python frontend.py

# Ensure that you have rebuilt the site and commited your changes
echo "Deploying to GitHub pages..."

# Create the subtree, push changes to gh-pages
git subtree push --prefix output origin gh-pages
