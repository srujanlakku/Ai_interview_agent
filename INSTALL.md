# InterviewPilot - Complete Installation & Reference Guide

## 📋 Project Overview

**InterviewPilot** is an enterprise-grade AI interview preparation platform that helps candidates succeed through:
- 🤖 Adaptive AI interviews with intelligent difficulty progression
- 📚 Multi-modal learning materials (text, images, videos)
- 🔍 Company-specific interview pattern research
- 📊 Advanced analytics and progress tracking
- 💾 AI-powered long-term memory system
- ✅ Production-grade reliability and error handling

---

## 🚀 Quick Start (< 5 minutes)

### Option A: Automated Startup (Recommended)

**Windows:**
```bash
# Double-click start.bat or run:
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Result:**
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000
- Database initialized automatically

### Option B: Docker Compose (One Command)

```bash
docker-compose up -d

# Wait 30-60 seconds for services to start
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## 📂 Project Structure

```
Interview-agent/
├── backend/                           # Python FastAPI backend
│   ├── app/
│   │   ├── agents/                   # AI agents (5 specialized agents)
│   │   │   ├── base_agent.py         # Base class with LLM integration
│   │   │   ├── research_agent.py     # Company research
│   │   │   ├── interviewer_agent.py  # Mock interviews
│   │   │   ├── evaluation_agent.py   # Performance scoring
│   │   │   ├── learning_agent.py     # Material generation
│   │   │   └── memory_agent.py       # Long-term memory
│   │   ├── api/
│   │   │   ├── auth_routes.py        # Authentication endpoints
│   │   │   ├── interview_routes.py   # Interview endpoints
│   │   │   ├── profile_routes.py     # Profile endpoints
│   │   │   └── memory_routes.py      # Memory endpoints
│   │   ├── models/
│   │   │   └── database.py           # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── schemas.py            # Pydantic validation schemas
│   │   ├── services/
│   │   │   ├── user_service.py       # User management
│   │   │   └── interview_service.py  # Interview management
│   │   ├── utils/
│   │   │   ├── database.py           # DB configuration
│   │   │   ├── security.py           # Password/JWT handling
│   │   │   ├── logging_config.py     # Logging setup
│   │   │   └── exceptions.py         # Custom exceptions
│   │   ├── config.py                 # Settings management
│   │   └── main.py                   # FastAPI app
│   ├── tests/
│   │   └── test_user_service.py      # Unit tests
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment template
│   ├── Dockerfile                     # Container image
│   └── .gitignore
│
├── frontend/                          # React Vite frontend
│   ├── src/
│   │   ├── pages/                    # Page components
│   │   │   ├── SignupPage.jsx        # Sign up page
│   │   │   ├── LoginPage.jsx         # Login page
│   │   │   ├── OnboardingPage.jsx    # Profile setup
│   │   │   └── DashboardPage.jsx     # Main dashboard
│   │   ├── components/               # Reusable components
│   │   ├── services/
│   │   │   └── api.js                # API client (Axios)
│   │   ├── utils/
│   │   │   └── store.js              # State management (Zustand)
│   │   ├── styles/
│   │   │   └── globals.css           # Global styles
│   │   ├── App.jsx                   # Main app component
│   │   └── main.jsx                  # Entry point
│   ├── package.json                  # npm dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── Dockerfile                    # Container image
│   ├── index.html                    # HTML template
│   └── .gitignore
│
├── docker-compose.yml                # Docker orchestration
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Quick start guide
├── DEPLOYMENT.md                      # Production deployment
├── ARCHITECTURE.md                    # System design doc
├── start.sh                           # Linux startup script
├── start.bat                          # Windows startup script
└── .gitignore                         # Git ignore rules
```

---

## ⚙️ System Requirements

### Minimum
- Python 3.9+
- Node.js 16+
- 2GB RAM
- 500MB disk space

### Recommended for Production
- Python 3.11+
- Node.js 18+
- 8GB RAM
- PostgreSQL 14+
- 10GB SSD
- Docker & Docker Compose

---

## 📦 Installation

### Step 1: Prerequisites

**Windows:**
```powershell
# Install Python 3.11
# https://www.python.org/downloads/

# Install Node.js 18 LTS
# https://nodejs.org/

# Verify installation
python --version  # Should show 3.9+
node --version    # Should show 16+
npm --version     # Should show 7+
```

**macOS:**
```bash
# Using Homebrew (install from https://brew.sh if needed)
brew install python@3.11
brew install node

# Verify
python3 --version
node --version
npm --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# Verify
python3 --version
node --version
npm --version
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# OR Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # macOS/Linux
# OR
copy .env.example .env  # Windows

# Edit .env and add your API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# (Optional) Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 4: Start Services

**Option A: Individual Terminals**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate  # macOS/Linux
python -m uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

**Option B: Docker Compose**
```bash
docker-compose up -d
docker-compose ps  # Check status
```

---

## 🔌 API Configuration

### Required API Keys

Get these from:

1. **OpenAI** (https://platform.openai.com/api-keys)
   - Required for GPT-3.5 questions and evaluation
   - Free tier: $5 credit

2. **Anthropic** (https://console.anthropic.com)
   - Fallback LLM for resilience
   - Optional but recommended

3. **Google Search** (https://serpapi.com)
   - For company-specific research
   - Optional (uses fallback knowledge if unavailable)

### .env Configuration

```env
# Essential
OPENAI_API_KEY=sk-your-key-here
SECRET_KEY=change-this-to-random-string-in-production

# Optional but recommended
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_SEARCH_API_KEY=your-key-here

# Database (local SQLite for development)
DATABASE_URL=sqlite:///./interview_pilot.db
# OR PostgreSQL for production
DATABASE_URL=postgresql://user:password@localhost:5432/interview_pilot

# Development settings
DEBUG=True
LOG_LEVEL=INFO
```

---

## 🧪 Testing

### Backend Unit Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_user_service.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Manual API Testing

```bash
# Health check
curl http://localhost:8000/health

# Interactive API docs
# Open http://localhost:8000/docs in browser

# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"Password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Password123"}'
```

---

## 🎯 Usage Walkthrough

### 1. Create Account
- Visit http://localhost:3000
- Click "Sign up"
- Enter email, name, password (must include uppercase + digit)
- Submit

### 2. Complete Onboarding
- Enter target company (e.g., "Google")
- Enter target role (e.g., "Senior Software Engineer")
- Select interview type (Technical/HR/Managerial/Mixed)
- Select experience level (Fresher/Junior/Mid/Senior)
- Set available prep hours (e.g., 20)
- Click "Start Preparation"

### 3. Dashboard Overview
- View interview history
- Check your average score
- See readiness level
- Review progress trends
- View upcoming topics to study

### 4. Start Mock Interview
- Click "Start New Interview"
- Answer AI-generated questions
- Get real-time feedback
- See difficulty adjust based on performance
- View final score and readiness assessment

### 5. Review Progress
- Check strengths and weaknesses
- View covered topics
- Focus on missed/weak areas
- Track improvement over time

---

## 🔧 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find process using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Kill process or use different port
python -m uvicorn app.main:app --port 8001
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Verify virtual environment is activated
which python  # Should show venv path
```

**Database errors:**
```bash
# Reset SQLite database
rm backend/interview_pilot.db
# Will be recreated on next run

# Or run migrations
python -m alembic upgrade head
```

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in backend/app/main.py
- Verify proxy in frontend/vite.config.js

**npm install fails:**
```bash
# Clear npm cache
npm cache clean --force

# Try install again
npm install

# Or use yarn
npm install -g yarn
yarn install
```

**Port 3000 in use:**
```bash
# Use different port
npm run dev -- --port 3001
```

### Docker Issues

**Containers won't start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild images
docker-compose build --no-cache

# Clean and restart
docker-compose down -v
docker-compose up -d
```

---

## 📊 Key Features Implementation

### ✅ Authentication
- Secure signup with password validation
- JWT token-based login (30-min expiry)
- Session management
- Password hashing with bcrypt

### ✅ User Profiles
- Company and role selection
- Interview type selection
- Experience level tracking
- Available hours for prep

### ✅ Research Agent
- Company-specific FAQ research
- Interview rounds analysis
- Evaluation criteria extraction
- Required skills identification
- Fallback to generalized knowledge

### ✅ Interview Simulation
- Adaptive difficulty progression
- Real-time question generation
- Instant answer evaluation
- Follow-up question generation
- Score calculation (0-10)

### ✅ Performance Tracking
- Per-question scoring
- Overall readiness assessment
- Historical progress tracking
- Strength/weakness profiling

### ✅ Memory System
- Long-term user memory
- Strength tracking
- Weakness identification
- Covered topics logging
- Missed topics flagging

### ✅ Learning Materials
- Multi-modal content (text, links)
- Relevance-based ranking
- Time-constrained adaptation
- Difficulty levels

---

## 🚀 Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- AWS deployment guide
- RDS database setup
- ECR container registry
- ECS service deployment
- CloudFront CDN setup
- Auto-scaling configuration
- Monitoring and alerting
- Disaster recovery

---

## 📚 Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for:
- High-level system architecture
- Data flow diagrams
- Agent responsibilities
- Security architecture
- Error handling strategy
- Performance considerations
- Scalability planning

---

## 📖 API Documentation

### Authentication Endpoints
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get profile

### Interview Endpoints
- `POST /api/interviews/create` - Start interview
- `GET /api/interviews/{id}` - Get details
- `POST /api/interviews/{id}/start-question` - Get question
- `POST /api/interviews/{id}/submit-answer` - Submit answer
- `POST /api/interviews/{id}/finalize` - Finish interview

### Profile Endpoints
- `POST /api/profile/onboard` - Setup profile
- `GET /api/profile/{id}` - Get profile
- `POST /api/profile/{id}/prepare` - Generate materials

### Memory Endpoints
- `GET /api/memory/{id}/summary` - Get memory
- `GET /api/memory/{id}/strengths` - Strengths
- `GET /api/memory/{id}/weaknesses` - Weaknesses

See http://localhost:8000/docs for interactive documentation.

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Zustand State Management](https://github.com/pmndrs/zustand)

---

## 📞 Support & Contributing

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join community discussions
- **Contributing**: See CONTRIBUTING.md
- **Email**: support@interviewpilot.com

---

## 📄 License

InterviewPilot is proprietary software. All rights reserved.

---

## 🎯 Next Steps

1. ✅ Installation complete!
2. 📝 Update `.env` with your API keys
3. 🚀 Start services using `start.sh` or `start.bat`
4. 🌐 Open http://localhost:3000
5. 📝 Create account and onboard
6. 💪 Start mock interview training!

---

**Built with ❤️ for interview success**
**v1.0.0 | January 28, 2026**
