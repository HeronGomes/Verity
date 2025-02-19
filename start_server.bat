@echo off
set PYTHONPATH=src
uvicorn main:app --reload
pause

