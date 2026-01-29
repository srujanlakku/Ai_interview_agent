# Quick Start Guide

## Option 1: Local Development (Recommended for Development)

### Prerequisites
- Python 3.9+ installed
- Node.js 16+ installed
- Git installed

### Step 1: Clone and Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # On Windows
cp .env.example .env    # On macOS/Linux

# Add your API keys to .env
# Edit .env and add:
# OPENAI_API_KEY=your_key
# ANTHROPIC_API_KEY=your_key
```

### Step 2: Run Backend

```bash
# From backend directory with venv activated
python -m uvicorn app.main:app --reload

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Step 3: Setup Frontend

In a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend runs at http://localhost:3000
```

## Option 2: Docker Deployment (Recommended for Production)

### Prerequisites
- Docker installed
- Docker Compose installed

### Single Command Deployment

```bash
# From project root
docker-compose up -d

# Wait for services to start (30-60 seconds)
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Check Status

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f backend    # Backend logs
docker-compose logs -f frontend   # Frontend logs

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Testing the Application

### 1. Create Account
- Go to http://localhost:3000
- Click "Sign up"
- Fill in details
- Submit

### 2. Onboard Profile
- After signup, set up your profile:
  - Target Company (e.g., "Google")
  - Target Role (e.g., "Software Engineer")
  - Interview Type (e.g., "Technical")
  - Experience Level (e.g., "Mid")
  - Available Hours (e.g., "20")

### 3. View Dashboard
- See your interview statistics
- View preparation progress
- Check readiness level

### 4. Start Interview
- Click "Start New Interview"
- Answer AI-generated questions
- Receive real-time feedback
- Get interview score and readiness assessment

## API Testing with Curl

### Health Check
```bash
curl http://localhost:8000/health
```

### Signup
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "Password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Password123"
  }'
```

## Environment Variables

### Backend (.env)
```
# Database
DATABASE_URL=sqlite:///./interview_pilot.db
# or PostgreSQL: postgresql://user:password@localhost:5432/interview_pilot

# Authentication
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Application
DEBUG=True
APP_TITLE=InterviewPilot
APP_VERSION=1.0.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Kill process or use different port
python -m uvicorn app.main:app --port 8001
```

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check CORS settings in backend/app/main.py
- Verify proxy settings in frontend/vite.config.js

### Database Issues
```bash
# Reset database (local SQLite)
rm interview_pilot.db

# Database will be recreated on next run
python -m uvicorn app.main:app --reload
```

### Docker Issues
```bash
# Rebuild containers
docker-compose build --no-cache

# View service logs for errors
docker-compose logs backend
docker-compose logs frontend
```

## Performance Optimization

### Backend
- Configured connection pooling
- Async operations for I/O
- Response caching where applicable
- Database indexing on frequently queried columns

### Frontend
- Code splitting with React Router
- Image optimization
- CSS minification in production
- Service worker for offline support (coming soon)

## Security Checklist

Before going to production:

- [ ] Change SECRET_KEY in .env
- [ ] Use strong, unique API keys
- [ ] Enable HTTPS/TLS
- [ ] Set DEBUG=False
- [ ] Configure proper CORS origins
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable rate limiting
- [ ] Set up API key rotation
- [ ] Enable request logging and monitoring
- [ ] Set up backup strategy for database

## Next Steps

1. **Customize Styling** - Update colors in `frontend/src/styles/globals.css`
2. **Add More Features** - Extend agents or add new functionality
3. **Setup Monitoring** - Integrate with monitoring tools like Sentry
4. **Configure CI/CD** - Setup GitHub Actions or similar
5. **User Management** - Implement roles and permissions
6. **Analytics** - Track usage and performance metrics

## Support & Resources

- API Documentation: http://localhost:8000/docs (when running)
- GitHub Issues: Report bugs and feature requests
- Stack Overflow: Tag questions with #interviewpilot

---

Happy interviewing! 🚀
