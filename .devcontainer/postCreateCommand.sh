#! /usr/bin/env bash

# Install fish terminal
sudo apt update -y
sudo apt-get install fish -y

# Repo Initialization
make init-repo
git config --global --add safe.directory /workspaces/resume-maker-ai-agent

# Install Dependencies
make reset-env
