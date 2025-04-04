#!/bin/bash
cd /home/xujus/Documents/ASU/Research/git
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github
ssh -T git@github.com
git branch -M main
git add /home/xujus/Documents/ASU/Research/git/*
git commit
git push -u configs main
