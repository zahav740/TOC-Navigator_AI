#!/usr/bin/env bash
set -e
python3 -m venv .venv || python -m venv .venv. .venv/bin/activate
python -m pip install --upgrade pip
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f requirements-dev.txt ] && pip install -r requirements-dev.txt
[ -d frontend ] && [ -f frontend/package.json ] && cd frontend && (npm ci || npm install) && cd ..
echo READY