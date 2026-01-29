# 🆘 TROUBLESHOOTING & ERROR RESOLUTION GUIDE

**Quick Solutions to Common Issues**

---

## 🔴 CRITICAL ERRORS

### Backend Won't Start

**Error**: `Address already in use` or `Port 8001 in use`

**Solution**:
```bash
# Find what's using port 8001
lsof -i :8001          # On Linux/Mac
netstat -ano | findstr :8001  # On Windows

# Kill the process
kill -9 <PID>          # On Linux/Mac
taskkill /PID <PID> /F # On Windows

# Or use different port
uvicorn app.main:app --port 8002
```

---

### Frontend Won't Connect to Backend

**Error**: `Failed to fetch from API` or `CORS error`

**Solution**:
```javascript
// Check API URL in frontend/src/js/api-client.js
// Should be: http://localhost:8001

// If on production, update to:
const API_BASE_URL = "https://api.yourdomain.com"

// Verify backend is running:
// Visit http://localhost:8001/docs in browser
```

---

### Database Connection Error

**Error**: `No module named 'sqlite3'` or `Database locked`

**Solution**:
```bash
# Install sqlite3
pip install sqlite3  # Usually comes with Python

# Check if database file exists
ls -la interview_pilot.db

# If locked, close other connections and try again
# If corrupted, restore from backup:
cp interview_pilot_backup.db interview_pilot.db
```

---

### Python Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt

# Verify installations
pip list
```

---

### JWT Token Invalid

**Error**: `401 Unauthorized` or `Invalid token`

**Solution**:
```bash
# Generate new JWT secret in .env
JWT_SECRET_KEY=<new-random-key>

# Clear browser localStorage (causes token issues)
# Open browser console (F12)
# Run: localStorage.clear()

# Try logging in again
```

---

## 🟡 COMMON WARNINGS

### SSL Certificate Warnings

**Issue**: `SSL: CERTIFICATE_VERIFY_FAILED` in development

**Solution**:
```python
# In development only, add to .env
SSL_VERIFY=False

# In production, proper certificates required:
# Use Let's Encrypt (free)
```

---

### CORS Errors in Frontend

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
```python
# In backend/app/main.py, check CORS config:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure frontend URL is in allow_origins
```

---

### Console Errors in Frontend

**Error**: `Cannot read property of undefined` or `TypeError`

**Solution**:
```javascript
// Open browser console (F12)
// Check the error message carefully

// Common issues:
// 1. API not responding → check backend
// 2. HTML element not found → check HTML ID
// 3. Token missing → clear localStorage and login again

// Debug by adding console.log:
console.log("API response:", response);
console.log("Current user:", auth.getCurrentUser());
```

---

## 🟢 PERFORMANCE ISSUES

### Website Loading Slow

**Solution**:
```bash
# Optimize frontend
# 1. Minimize CSS/JS files
# 2. Compress images
# 3. Enable caching headers
# 4. Use CDN for static files

# Check network tab in browser (F12)
# Look for slow requests and large files
```

---

### Backend API Slow

**Solution**:
```python
# Check database queries
# Add logging to see slow queries
import time

start = time.time()
# your query here
end = time.time()
print(f"Query took {end - start}s")

# Optimize indexes if needed
# Add caching for repeated queries
```

---

### High Memory Usage

**Solution**:
```bash
# Check what's using memory
# Linux: top, htop
# Windows: Task Manager

# Restart services
sudo systemctl restart interview-pilot-backend

# Check for memory leaks in code
# Use: memory_profiler package
```

---

## 🔵 DEPLOYMENT ISSUES

### 502 Bad Gateway

**Issue**: Nginx/proxy can't reach backend

**Solution**:
```bash
# Check if backend is running
curl http://localhost:8001/health

# Check nginx logs
tail -f /var/log/nginx/error.log

# Verify nginx proxy config
# Proxy should forward to http://localhost:8001

# Restart nginx
sudo systemctl restart nginx
```

---

### Certificate Expired

**Issue**: `SSL_ERROR_BAD_CERT_DOMAIN` or similar

**Solution**:
```bash
# Check certificate expiry
openssl x509 -in /path/to/cert.pem -text -noout | grep -A 2 "Validity"

# Renew with Let's Encrypt
sudo certbot renew

# Or force renewal
sudo certbot renew --force-renewal

# Restart web server
sudo systemctl restart nginx
```

---

### 404 Not Found

**Issue**: Page not found when accessing routes

**Solution**:
```bash
# For frontend SPA, configure web server:
# Nginx should rewrite all requests to index.html

location / {
    try_files $uri $uri/ /index.html;
}

# Then restart
sudo systemctl restart nginx
```

---

## 🟠 DATA ISSUES

### Lost Data / Corrupted Database

**Recovery**:
```bash
# 1. Stop backend
sudo systemctl stop interview-pilot-backend

# 2. Check backup location
ls -la /backups/interview-pilot/

# 3. Restore from backup
cp /backups/interview-pilot/interview_pilot_backup.db /opt/interview-pilot/interview_pilot.db

# 4. Verify restoration
sqlite3 interview_pilot.db "SELECT COUNT(*) FROM users;"

# 5. Start backend
sudo systemctl start interview-pilot-backend
```

---

### User Data Not Saving

**Issue**: Form submits but data doesn't appear

**Solution**:
```javascript
// Check browser console for errors
// 1. Network tab → check API response
// 2. Application tab → check localStorage
// 3. Backend logs → check for database errors

// Debug steps:
console.log("Form data:", formData);
console.log("API response:", apiResponse);
console.log("Database:", localStorage);
```

---

### Password Reset Not Working

**Issue**: User can't reset password

**Solution**:
```bash
# If using password reset, verify email service:
# Check SMTP configuration in .env
# SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

# Test email sending
python -c "
import smtplib
smtp = smtplib.SMTP('your-smtp-server', 587)
smtp.starttls()
# If no error, SMTP works
"
```

---

## 🟣 SECURITY ISSUES

### Suspected Breach / Unauthorized Access

**Action Plan**:
```bash
# 1. Immediately revoke all tokens
# Update JWT_SECRET_KEY in .env

# 2. Check access logs
sudo tail -f /var/log/interview-pilot/app.log | grep -i "error\|failed"

# 3. Change database password if PostgreSQL

# 4. Review user accounts
sqlite3 interview_pilot.db "SELECT * FROM users WHERE created_at > date('now', '-1 day');"

# 5. Force password reset for all users

# 6. Run security audit
# See BEST_PRACTICES_GUIDE.md for security checks
```

---

### Suspicious API Activity

**Investigation**:
```bash
# Check API logs for:
# 1. Too many requests from single IP
# 2. Failed login attempts
# 3. Invalid tokens
# 4. Unusual data access patterns

# Example: Check failed logins
grep "login" /var/log/interview-pilot/app.log | grep -i "failed" | wc -l

# Enable rate limiting if needed (add to requirements.txt):
# slowapi
```

---

## 📋 DIAGNOSTICS CHECKLIST

When something breaks, check in order:

### 1. Backend Status
```bash
[ ] Backend process running?          sudo systemctl status interview-pilot-backend
[ ] Backend listening on 8001?         netstat -tulpn | grep 8001
[ ] Backend logs for errors?           journalctl -u interview-pilot-backend -n 50
[ ] Database accessible?               sqlite3 interview_pilot.db ".tables"
[ ] Environment variables set?         cat .env | grep "^[A-Z]"
```

### 2. Frontend Status
```bash
[ ] Frontend loads?                    curl http://localhost:8080
[ ] Browser console errors?            F12 → Console tab
[ ] Network requests succeeding?       F12 → Network tab
[ ] LocalStorage intact?               F12 → Application tab
[ ] API URL correct?                   Check api-client.js
```

### 3. Network Status
```bash
[ ] Can ping backend server?           ping backend-ip
[ ] Firewall allowing ports?           sudo ufw status
[ ] Nginx running?                     sudo systemctl status nginx
[ ] DNS resolving?                     nslookup yourdomain.com
[ ] SSL certificate valid?             openssl s_client -connect yourdomain.com:443
```

### 4. Database Status
```bash
[ ] Database file exists?              ls -la interview_pilot.db
[ ] Database accessible?               sqlite3 interview_pilot.db ".schema"
[ ] Tables created?                    sqlite3 interview_pilot.db ".tables"
[ ] Data intact?                       sqlite3 interview_pilot.db "SELECT COUNT(*) FROM users;"
[ ] Backup exists?                     ls -la /backups/interview-pilot/
```

---

## 🔧 COMMON FIXES

### Quick Restart Everything
```bash
# Backend
sudo systemctl restart interview-pilot-backend

# Frontend
sudo systemctl restart nginx

# Or for development:
# Kill all Python processes
pkill -f "python.*uvicorn"

# Restart backend
python -m uvicorn app.main:app --reload

# Restart frontend (new terminal)
cd frontend && python -m http.server 8080
```

---

### Clear Cache & Cookies
```javascript
// In browser console (F12)
localStorage.clear();
sessionStorage.clear();

// For cookies
document.cookie.split(";").forEach(c => {
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
});

// Then refresh page
location.reload();
```

---

### Rebuild Frontend Assets
```bash
# If CSS/JS not updating
cd frontend

# Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)

# Or from server:
# Add cache-busting to index.html
# <link rel="stylesheet" href="src/css/base.css?v=1.0">
# (increment version number)

# Then reload in browser
```

---

### Reset Database to Clean State
```bash
# ⚠️ WARNING: This deletes all data!

cd /opt/interview-pilot

# Backup current database
cp interview_pilot.db interview_pilot_backup_$(date +%s).db

# Remove database
rm interview_pilot.db

# Recreate tables
python -c "
from app.utils.database import Base, engine
Base.metadata.create_all(engine)
print('Database reset to clean state')
"

# Restart backend
sudo systemctl restart interview-pilot-backend
```

---

## 📞 WHEN TO ESCALATE

If issue persists after trying above solutions:

### Escalation Path
```
1. Check all documentation files:
   - SETUP_GUIDE.md
   - BEST_PRACTICES_GUIDE.md
   - PROJECT_QUALITY_AUDIT.md

2. Review relevant logs:
   - /var/log/interview-pilot/app.log
   - Browser console (F12)
   - Nginx error logs

3. Search error message online:
   - Stack Overflow
   - GitHub Issues
   - Official documentation

4. If custom issue:
   - Create minimal reproduction
   - Document steps taken
   - Contact technical support
```

---

## 🎯 PREVENTION TIPS

### Avoid Common Issues
```
✅ Always keep backups
✅ Monitor logs regularly
✅ Keep dependencies updated
✅ Test after configuration changes
✅ Use version control (git)
✅ Document all changes
✅ Set up monitoring alerts
✅ Regular security audits
✅ Test disaster recovery monthly
✅ Update documentation
```

---

## 📊 ISSUE SEVERITY LEVELS

| Severity | Impact | Response Time | Examples |
|----------|--------|---|----------|
| Critical | 🔴 Service down | Immediate | Backend crash, DB loss, data breach |
| High | 🟠 Major feature broken | 1 hour | Login not working, data missing |
| Medium | 🟡 Minor feature broken | 4 hours | Some pages slow, cosmetic issues |
| Low | 🟢 Cosmetic issue | 1 day | Text alignment, color inconsistency |

---

## 📚 HELPFUL RESOURCES

**For Each Issue Type**:
- Backend Errors → Check SETUP_GUIDE.md
- Frontend Errors → Check FRONTEND_README.md
- Deployment Issues → Check PRODUCTION_DEPLOYMENT_CHECKLIST.md
- Security Issues → Check BEST_PRACTICES_GUIDE.md
- Performance Issues → Check code directly
- Database Issues → Check SETUP_GUIDE.md Database section

---

## ✅ ISSUE RESOLVED CHECKLIST

After fixing any issue:
```
[ ] Document the issue and solution
[ ] Add to this guide if not present
[ ] Test to ensure it's fixed
[ ] Monitor for recurrence
[ ] Update monitoring alerts if needed
[ ] Communicate to team
[ ] Update backup if needed
[ ] Review if preventable
```

---

## 💡 KEY REMINDERS

1. **Always backup before major changes**
2. **Read error messages carefully** (they usually point to the solution)
3. **Check logs first** (they contain the answer)
4. **Restart services after config changes**
5. **Test locally before deploying**
6. **Keep documentation updated**
7. **Monitor system regularly**
8. **Have recovery plan ready**

---

**Last Updated**: January 28, 2026
**Version**: 1.0
**Status**: Ready for Use ✅

*For most recent troubleshooting tips, check the GitHub issues or contact support.*

