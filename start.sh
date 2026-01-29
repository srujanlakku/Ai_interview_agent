#!/bin/bash

# InterviewPilot Quick Start Script

echo "🚀 Starting InterviewPilot..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check Node
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

echo ""
echo "📦 Setting up backend..."

# Backend setup
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ .env file created. Please update with your API keys${NC}"
fi

# Install dependencies
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Start backend
echo -e "${GREEN}✓ Starting backend server...${NC}"
python -m uvicorn app.main:app --reload &
BACKEND_PID=$!

cd ..

echo ""
echo "📦 Setting up frontend..."

# Frontend setup
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    npm install -q
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Frontend dependencies already exist${NC}"
fi

# Start frontend
echo -e "${GREEN}✓ Starting frontend server...${NC}"
npm run dev &
FRONTEND_PID=$!

cd ..

# Wait for services to start
sleep 3

echo ""
echo -e "${GREEN}✅ InterviewPilot started successfully!${NC}"
echo ""
echo "📍 Services running:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "⚙️ Next steps:"
echo "   1. Update backend/.env with your API keys"
echo "   2. Open http://localhost:3000 in your browser"
echo "   3. Create an account and start preparing"
echo ""
echo "💡 Tips:"
echo "   - Backend logs: See output above"
echo "   - Frontend logs: Check terminal running npm"
echo "   - Database: SQLite file at backend/interview_pilot.db"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID
    echo "✓ Services stopped"
}

# Register cleanup
trap cleanup EXIT

# Wait for both processes
wait
