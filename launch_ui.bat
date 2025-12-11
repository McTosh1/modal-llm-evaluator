@echo off
echo Starting LLM Evaluator Web Interface...
echo.
echo Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
streamlit run streamlit_app/app.py
