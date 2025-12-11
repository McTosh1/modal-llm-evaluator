#!/bin/bash

echo "Starting LLM Evaluator Web Interface..."
echo ""
echo "Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
streamlit run streamlit_app/app.py
