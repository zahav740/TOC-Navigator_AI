#!/usr/bin/env bash
set -e. .venv/bin/activate || true
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f requirements-dev.txt ] && pip install -r requirements-dev.txt
echo OK