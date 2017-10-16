#!/bin/bash

echo "Changing directory and pulling from source..."
repo="git@github.com:galvinma/pythia.git"
if [ -d ".git" ]; then
  echo "This directory has already been initialized with git. Pulling latest master..."
  git pull origin master
else
  git init .
  git remote add origin "https://github.com/galvinma/pythia.git"
  git pull origin master
fi

echo "Removing old virtualenv..."
rm -rf "/home/galvinma/.virtualenvs/jenkinspythia/"

echo "Creating directory if DNE..."
if [ ! -d "/home/galvinma/.jenkins/workspace/pythia/" ]; then
  mkdir -p "/home/galvinma/.jenkins/workspace/pythia/"
fi

echo "Creating virtual env and installing requirements..."
cd "/home/galvinma/.jenkins/workspace/pythia/"
pip install virtualenv
virtualenv jenkinspythia
cd "/home/galvinma/.jenkins/workspace/pythia/jenkinspythia/bin/"
source activate

cd "/home/galvinma/.jenkins/workspace/pythia/"
pip install -r requirements.txt

echo "Executing Pythia and associated tests..."
python view.py &
python sel.py
exit 0
