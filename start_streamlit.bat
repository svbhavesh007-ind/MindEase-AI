@echo off
echo ========================================================
echo   Starting MindEase Streamlit Interface
echo ========================================================
echo.

IF EXIST venv\Scripts\streamlit.exe (
    venv\Scripts\streamlit.exe run streamlit_app.py
) ELSE (
    streamlit run streamlit_app.py
)

pause
