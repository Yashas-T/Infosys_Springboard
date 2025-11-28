#!/bin/bash
set -e

# Start the FastAPI backend in the background
echo "Starting FastAPI Backend..."
uvicorn backend.model_server:app --host 0.0.0.0 --port 8000 &

# Wait a few seconds for the backend to initialize
sleep 5

# Start the Streamlit frontend
echo "Starting Streamlit App..."
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
