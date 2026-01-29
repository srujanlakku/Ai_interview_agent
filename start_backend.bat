@echo off
cd /d "g:\projects\Interview-agent\backend"
"g:\projects\Interview-agent\venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --log-level info
