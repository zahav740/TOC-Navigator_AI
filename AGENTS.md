# AGENTS.md
## Setup
python3 -m venv .venv
. .venv/Scripts/Activate.ps1
pip install --upgrade pip
if (Test-Path requirements.txt) { pip install -r requirements.txt }
if (Test-Path requirements-dev.txt) { pip install -r requirements-dev.txt }
## Dev
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
python -m http.server 5173 --directory frontend
## Test
pytest -q
