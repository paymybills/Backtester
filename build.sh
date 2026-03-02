#!/usr/bin/env bash
# Render deployment build script
set -o errexit

# Install dependencies
pip install -r requirements.txt
