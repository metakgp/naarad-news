import shlex
import subprocess
import os


def deploy():
    print("Deploying to GitHub pages...")

    # Deploy command works only because I've cloned another version of the repo
    # there and checkout the gh-pages branch

    os.chdir("output")

    commands = [
        "git add *",
        "git commit -m \"Build\"",
        "git push -f origin gh-pages"
            ]

    for cmd in commands:
        subprocess.call(shlex.split(cmd))
