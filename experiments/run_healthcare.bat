@echo off
call "C:\Users\Anurup R Krishnan\miniconda3\Scripts\activate.bat" edge
cd /d "%~dp0"
python healthcare_evaluation.py
pause