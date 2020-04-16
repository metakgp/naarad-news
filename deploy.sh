#!/bin/bash
# source /home/pi/.bashrc
# git remote update
# git rebase origin/master
# source /home/pi/naarad_venv/bin/activate
echo "Naarad Muni will take a nap for half an hour. Do not disturb."
#sleep 9m
echo "Slept for 9 minutes"
#sleep 9m
echo "Slept for another 9 minutes"
#sleep 9m
echo "Again slept for 9 minutes"
git remote add origin-here https://${OUATH_KEY}@github.com/americast/naarad-source.git
git fetch origin-here
python3 fbscraper.py
#python3 frontend.py
# deactivate
# # Commit changes
# echo "commiting.."
# git add -A
# git commit --amend --no-edit

# # Create the subtree, push changes to gh-pages
# # git subtree split --prefix output -b gh-pages

# echo "deploying.."
# git push -f origin master
# # git push -f origin gh-pages:gh-pages

# echo "cleaning..."
# git branch -D gh-pages
