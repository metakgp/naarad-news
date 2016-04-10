#!/bin/bash

# Ensure that you have rebuilt the site and commited your changes
echo "Deploying to GitHub pages..."

# Create the subtree
cd output
# git subtree split --prefix output -b gh-pages
# Push to origin
git add *
git commit -m "Build"
git push -f origin gh-pages
# Remove so that later the process can be repeated
# Push master

# nikola github_deploy
# git checkout master
