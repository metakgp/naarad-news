#!/bin/bash
python3 fbscraper.py
#python3 frontend.py

# Commit changes
echo "commiting.."
git add -A
git commit -m 'Update and Build'

# Create the subtree, push changes to gh-pages
# git subtree split --prefix output -b gh-pages

echo "deploying.."
git push origin master
# git push -f origin gh-pages:gh-pages

# echo "cleaning..."
# git branch -D gh-pages
