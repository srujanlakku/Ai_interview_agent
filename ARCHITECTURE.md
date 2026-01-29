# System Architecture & Design Document

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Browser (Frontend)                      │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  React SPA (Vite)                                        │   │
│  │  - Authentication Flow                                   │   │
│  │  - Dashboard & Analytics                                 │   │
│  │  - Interview Interface                                   │   │
│  │  - Study Materials Viewer                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Server                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Routes Layer                                        │  │
│  │  - /api/auth/* (Authentication)                         │  │
│  │  - /api/interviews/* (Interview Management)             │  │
│  │  - /api/profile/* (User Profile)                        │  │
│  │  - /api/memory/* (Memory Management)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Services Layer                                          │  │
│  │  - UserService                                           │  │
│  │  - InterviewService                                      │  │
│  │  - Research & LearningServices                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AI Agents Layer                                         │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ ResearchAgent (Company-Specific Research)         │ │  │
│  │  │ InterviewerAgent (Mock Interviews)                │ │  │
│  │  │ EvaluationAgent (Score & Feedback)                │ │  │
│  │  │ LearningAgent (Material Generation)               │ │  │
│  │  │ MemoryAgent (Long-term Knowledge)                 │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LLM Interface (Base Agent)                             │  │
│  │  - OpenAI GPT-3.5 (Primary)                            │  │
│  │  - Anthropic Claude (Fallback)                         │  │
│  │  - Retry Logic & Error Handling                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ PostgreSQL   │  │ Redis Cache  │  │ File Storage │
    │ Database     │  │ (Optional)   │  │ (Images, etc)│
    └──────────────┘  └──────────────┘  └──────────────┘
```

## Data Flow

### Interview Flow

```
1. User Onboards
   └─> Profile Created
       └─> Research Agent Triggered (async)
           └─> Company patterns researched
           └─> Learning materials generated

2. User Starts Interview
   └─> Interviewer Agent Initializes
       └─> Question Generated (adaptive difficulty)
       └─> User Answers
           └─> Evaluation Agent Scores
           └─> Difficulty Adjusted
           └─> Memory Updated
           └─> Next Question Generated (or finalized)

3. Interview Completes
   └─> Final Scores Calculated
   └─> Feedback Generated
   └─> Memory Updated with strengths/weaknesses
   └─> Readiness Level Updated
   └─> Historical Analytics Updated
```

### Memory System Flow

```
┌─────────────────────┐
│  Interview Session  │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────────────────────┐
    │ Evaluation Results           │
    │ - Per-question scores        │
    │ - Strengths identified       │
    │ - Weaknesses identified      │
    │ - Topics covered/missed      │
    └──────────────────────────────┘
           │
           ▼
    ┌──────────────────────────────┐
    │ Memory Agent                 │
    │ - Stores strengths           │
    │ - Stores weaknesses          │
    │ - Stores covered topics      │
    │ - Stores missed topics       │
    └──────────────────────────────┘
           │
           ├──────────────────┬──────────────────┐
           ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ User     │      │ Future   │      │ Analytics│
    │ Memory   │      │ Prep     │      │ Dashboard│
    │ Profile  │      │ Plans    │      │ Updates  │
    └──────────┘      └──────────┘      └──────────┘
```

## Agent Responsibilities

### ResearchAgent
- **Input**: Company name, Job role
- **Output**: Interview patterns, FAQ, skills, technologies
- **Fallback**: Generalized role-based knowledge
- **Caching**: Results cached for 7 days

### InterviewerAgent
- **Input**: User profile, Research data, Previous answers
- **Output**: Interview questions, Follow-ups
- **Adaptive**: Difficulty increases/decreases based on performance
- **Scoring**: Each answer scored immediately

### EvaluationAgent
- **Input**: Interview responses, Question context
- **Output**: Scores, Feedback, Readiness level
- **Metrics**: Technical accuracy, Clarity, Communication, Structure
- **Explainability**: Every score has justification

### LearningAgent
- **Input**: Required skills, Available time, Experience level
- **Output**: Ranked learning materials
- **Multi-modal**: Text, images, videos, links
- **Adaptive**: Customized to user constraints

### MemoryAgent
- **Input**: Interview results, User history
- **Output**: Strength/weakness profiles, Improvement plans
- **Persistence**: Database-backed long-term memory
- **Analytics**: Trend analysis over time

## Security Architecture

```
┌────────────────┐
│   User Login   │
└────────┬───────┘
         │
         ▼
┌────────────────────────┐
│ Password Hashing       │
│ (bcrypt + salt)        │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ JWT Token Generation   │
│ (HS256, 30 min exp)    │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Token Validation       │
│ (Every request)        │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ User Context Access    │
│ (Rate limited)         │
└────────────────────────┘
```

## Error Handling Strategy

### Retry Policy
- **Max Retries**: 3
- **Backoff**: Exponential (2^attempt seconds)
- **Timeout**: 30 seconds per request
- **Fallback**: Graceful degradation

### Error Categories

```python
{
  "LLMError": "Use fallback LLM",
  "SpeechRecognitionError": "Fallback to text-only",
  "ResearchError": "Use cached/generalized data",
  "DatabaseError": "Return cached results",
  "ValidationError": "Return 400 with details",
  "AuthenticationError": "Return 401 Unauthorized"
}
```

### Logging Strategy
- **Level**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Format**: `timestamp - logger_name - level - message`
- **Storage**: File + Console (rotating files, 10MB max)
- **Retention**: 30 days of logs

## Database Schema

```sql
-- Core Tables
users (id, email, password_hash, full_name, created_at)
user_profiles (id, user_id, company, role, interview_type, experience_level)
interviews (id, user_id, type, score, readiness_level, feedback)
interview_questions (id, interview_id, question, answer, score, feedback)

-- Memory Tables
user_memory (id, user_id, memory_type, content, metadata)
company_research (id, company_name, role, faq, rounds, criteria, skills)

-- Content Tables
preparation_materials (id, user_id, topic, type, content, relevance_score)

-- Indexes
idx_users_email (unique)
idx_interviews_user_id
idx_user_memory_user_id
idx_company_research_company_role
```

## Performance Considerations

### Caching Strategy
- Research results: 7-day TTL
- User memories: 1-day TTL
- Learning materials: 3-day TTL
- Session data: 30-minute TTL (Redis)

### Query Optimization
- Pagination for list endpoints
- Lazy loading of materials
- Index on frequently queried columns
- Avoid N+1 queries with joins

### Asynchronous Operations
- Research generation (background task)
- Learning material generation (background)
- Evaluation (can be async for batch jobs)
- Notification sending (async)

## Scalability Plan

### Horizontal Scaling
- Stateless API servers (can scale to N)
- Load balancer (ALB) for traffic distribution
- Redis cluster for distributed caching
- PostgreSQL with read replicas

### Vertical Scaling
- Increase server resources as needed
- Database connection pooling
- Query optimization
- Memory limits for cache

### Expected Growth
- **Year 1**: 10K users, 2 servers
- **Year 2**: 100K users, 5-10 servers
- **Year 3**: 1M users, 20-50 servers

## Monitoring & Observability

### Key Metrics
- Request latency (p50, p95, p99)
- Error rate (per endpoint)
- LLM API latency
- Database query time
- Cache hit rate
- User engagement metrics

### Alerting Thresholds
- Error rate > 5%
- Latency p99 > 5 seconds
- CPU > 80%
- Memory > 85%
- Database connections > 80%

### Dashboards
- Real-time status (Grafana/Datadog)
- Historical analytics
- Performance trends
- User funnel analysis

## Future Enhancements

1. **Multi-language Support**: Support interviews in multiple languages
2. **Advanced Video Interviews**: Webcam recording and playback
3. **Company Integrations**: Direct connection to job portals
4. **Mobile App**: Native iOS/Android apps
5. **Advanced Analytics**: ML-based performance predictions
6. **Team Features**: Group mock interviews with peers
7. **Certification Program**: Prepare for specific certifications
8. **Live Coaching**: Real human coaching integration

---

**Document Version**: 1.0  
**Last Updated**: January 28, 2026  
**Next Review**: Q2 2026
