@echo off
REM Activate the virtual environment and run uvicorn with FastAPI app
call "D:\FastAPI\learn FastAPI\app\VENV_EVENT\Scripts\activate.bat" &&  python -m uvicorn main:app --reload
