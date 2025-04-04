#!/bin/bash
cd /home/xujus/Documents/configsGit
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github
ssh -T git@github.com
git remote add configs git@github.com:JX518/newRepo.git
git branch -M main
git add /home/xujus/Documents/configsGit/*
git commit
git push -u configs main
