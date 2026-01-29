#!/bin/bash
# InterviewPilot Backend Startup Script

cd "$(dirname "$0")/backend"

echo "================================"
echo "InterviewPilot Backend Server"
echo "================================"
echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "ReDoc: http://localhost:8000/redoc"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
