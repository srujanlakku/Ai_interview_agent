# 🚀 INTERVIEWPILOT - QUICK START CARD

## ✅ Current Status
Backend is **RUNNING** on http://localhost:8001 ✅

## 🔗 Important Links
- **Swagger API Docs**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **OpenAPI Schema**: http://localhost:8001/openapi.json

## 🎯 Test the API Immediately

1. **Open Swagger**: http://localhost:8001/docs
2. **Sign up**: Click POST `/api/auth/signup`
   - Email: test@example.com
   - Password: Test123!@#
3. **Login**: Click POST `/api/auth/login` 
   - Use the same credentials
   - Copy the access token
4. **Authorize**: Click "Authorize" button, paste token as: `Bearer YOUR_TOKEN`
5. **Try other endpoints**: They're all documented!

## 📋 Available Endpoints

### Authentication
- `POST /api/auth/signup` - Register
- `POST /api/auth/login` - Login (get JWT token)
- `GET /api/auth/me` - Get current user

### Interviews
- `POST /api/interviews/create` - Create mock interview
- `GET /api/interviews/` - List interviews
- `GET /api/interviews/{id}/questions` - Get questions
- `POST /api/interviews/{id}/submit` - Submit answer
- `POST /api/interviews/{id}/finalize` - End interview & get evaluation

### Profile
- `POST /api/profile/onboard` - Onboard user
- `GET /api/profile/get` - Get profile

### Memory
- `GET /api/memory/summary` - Get user memory
- `GET /api/memory/strengths` - Get strengths
- `GET /api/memory/weaknesses` - Get weaknesses

## 🔧 To Restart Backend

**Windows (batch script):**
```batch
g:\projects\Interview-agent\start_backend.bat
```

**Windows (PowerShell):**
```powershell
cd g:\projects\Interview-agent\backend
..\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

**Mac/Linux:**
```bash
cd backend
../venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

## 📦 Directory Structure
```
Interview-agent/
├── backend/               ← Python FastAPI backend ✅ RUNNING
│   ├── app/main.py       ← API entry point
│   ├── app/api/          ← Route handlers
│   ├── app/agents/       ← AI agents
│   ├── app/models/       ← Database models
│   └── interview_pilot.db ← SQLite database
├── frontend/             ← React frontend (needs npm install)
├── venv/                 ← Python environment
└── start_backend.bat     ← Start script
```

## ⚙️ Configuration

**Backend defaults:**
- Port: 8001
- Host: 127.0.0.1 (localhost only)
- Database: SQLite (interview_pilot.db)
- JWT Secret: Hardcoded (change for production!)
- Token Expiry: 30 minutes

**To change port:**
```bash
python -m uvicorn app.main:app --port 8002
```

## 🔐 Authentication Flow

1. **Sign up** → Create user account (email + password)
2. **Login** → Get JWT access token
3. **Use token** → Add to request headers: `Authorization: Bearer TOKEN`
4. **Token expires** → Get refresh token or login again

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8001 in use | Kill process or use `--port 8002` |
| Database locked | Delete `interview_pilot.db`, restart |
| "Module not found" | `venv\Scripts\pip.exe list`, reinstall if needed |
| Server won't start | Check Python version: `python --version` |
| API returns 401 | Check JWT token is valid and not expired |

## 📊 Database
- **Type**: SQLite (development)
- **Location**: `backend/interview_pilot.db`
- **Tables**: 8 (user, interview, memory, etc.)
- **Auto-create**: Yes, on first startup

## 🤖 AI Agents Ready
1. ResearchAgent - Company research
2. InterviewerAgent - Generate questions
3. EvaluationAgent - Score performance
4. MemoryAgent - Store user data
5. LearningAgent - Generate content
6. BaseAgent - LLM wrapper

## 📝 Example: Complete Interview Flow

```bash
# 1. Sign up
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Test123!@#"}'

# 2. Login  
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Test123!@#"}'
# Response includes: {"access_token":"...", "token_type":"bearer"}

# 3. Use token in headers
curl -X GET http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. Create interview
curl -X POST http://localhost:8001/api/interviews/create \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Google","role":"Senior Engineer"}'
```

## ✨ Next Steps
1. ✅ Backend working → Test via Swagger UI
2. ⏳ Install frontend → `npm install && npm run dev`
3. ⏳ Create first interview → Use API to test flow
4. ⏳ Deploy to production → See DEPLOYMENT.md

## 📞 Support
- Check logs in terminal running backend
- Visit http://localhost:8001/docs for interactive testing
- See PROJECT_COMPLETE.md for full documentation
- See DEPLOYMENT.md for production setup

---
**Backend Status**: 🟢 OPERATIONAL
**Ready to build**: YES ✅
**Last updated**: 2026-01-28 16:10:00
