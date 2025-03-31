@echo off
cd /d %~dp0packages\vertice
call venv\Scripts\activate
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
