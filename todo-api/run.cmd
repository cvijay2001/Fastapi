@echo off
REM Activate the virtual environment and run uvicorn with FastAPI app
call "D:\learn FastAPI\todo-api\myenv\Scripts\activate.bat" && python -m uvicorn main:app --reload
