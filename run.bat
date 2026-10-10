@echo off
echo ========================================================
echo   Starting MindEase: Emotion-Aware Mental Wellness Companion
echo ========================================================
echo.

IF EXIST venv\Scripts\python.exe (
    venv\Scripts\python.exe run.py
) ELSE (
    python run.py
)

pause
