#!/bin/bash

echo "Changing directory and pulling from source.."
cd /home/galvinma/Workspace/jenkins/pythia/
repo="git@github.com:galvinma/pythia.git"
testdir="/home/galvinma/Workspace/jenkins/pythia/"
git init .
if [ -d ".git" ]; then
  echo "This directory has already been initialized with git."
  git pull origin master
else
  git remote add origin "https://github.com/galvinma/pythia.git"
  git pull origin master
fi

echo "Creating virtual env and installing requirements..."
mkvirtualenv jenkinspythia -a "/home/galvinma/Workspace/jenkins/pythia/"
pip install -r requirements.txt

echo "Executing Pythia and associated tests..."
ls
python sel.py
exit 0
