#!/usr/bin/env python
"""Test app to diagnose startup issues"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("1. Testing imports...")
try:
    from fastapi import FastAPI
    print("✓ FastAPI imported")
    from fastapi.middleware.cors import CORSMiddleware
    print("✓ CORS imported")
    from app.utils.database import init_db
    print("✓ init_db imported")
    from app.utils.logging_config import setup_logging
    print("✓ setup_logging imported")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

print("\n2. Testing database initialization...")
try:
    setup_logging()
    init_db()
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Testing model imports...")
try:
    from app.models import interview_data
    print("✓ interview_data imported")
    from app.models.database import User, UserProfile, UserMemory, Interview
    print("✓ All models imported")
except Exception as e:
    print(f"✗ Model import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Testing route imports...")
try:
    from app.api import auth_routes
    print("✓ auth_routes imported")
    from app.api import interview_routes
    print("✓ interview_routes imported")
    from app.api import intelligence_routes
    print("✓ intelligence_routes imported")
except Exception as e:
    print(f"✗ Route import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n5. Testing app creation...")
try:
    app = FastAPI(
        title="InterviewPilot",
        description="Enterprise-grade AI interviewer platform",
        version="1.0.0"
    )
    print("✓ App created")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("✓ CORS middleware added")
    
    app.include_router(auth_routes.router)
    print("✓ auth_routes included")
    app.include_router(interview_routes.router)
    print("✓ interview_routes included")
    app.include_router(intelligence_routes.router)
    print("✓ intelligence_routes included")
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    print("✓ Health endpoint added")
    
except Exception as e:
    print(f"✗ App creation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All tests passed! App is ready to run.")
print("Run with: uvicorn test_app:app --host 127.0.0.1 --port 8080")
