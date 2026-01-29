# 🚀 InterviewPilot Frontend - Getting Started Guide

**Visual step-by-step guide to get the frontend running immediately.**

---

## 📍 You Are Here

```
Project: InterviewPilot (AI Interview Platform)
Component: Frontend UI
Status: ✅ COMPLETE & READY TO RUN
Location: g:\projects\Interview-agent\frontend\
```

---

## ⏱️ Time Required

- **Start**: 2 minutes
- **First test**: 5 minutes
- **Full verification**: 15 minutes
- **Deployment**: 30 minutes

---

## ✅ Prerequisites Check

Before starting, verify:

```
☑ Backend running on http://localhost:8001
  → Open in browser and check Swagger UI loads
  → Or run: curl http://localhost:8001/docs

☑ Modern browser installed
  → Chrome, Firefox, Safari, or Edge (latest version)
  
☑ This folder location
  → g:\projects\Interview-agent\frontend\
  → All files present (see file list below)
```

---

## 📁 File Verification

**You should have these files:**

```
frontend/
✓ index.html                    ← Main entry point
✓ src/css/base.css             ← Theme & colors
✓ src/css/code-rain.css        ← Animation styles
✓ src/css/components.css       ← UI components
✓ src/css/pages.css            ← Page layouts
✓ src/css/responsive.css       ← Mobile styles
✓ src/js/code-rain.js          ← Animation engine
✓ src/js/api-client.js         ← API client
✓ src/js/router.js             ← Page router
✓ src/js/auth.js               ← Auth manager
✓ src/js/main.js               ← Pages & events
✓ README.md                     ← Documentation
✓ QUICK_START.md               ← Quick reference
✓ SETUP_GUIDE.md               ← Full setup
✓ TESTING_CHECKLIST.md         ← Testing guide
✓ PROJECT_SUMMARY.md           ← Project status
```

**If any are missing:**
1. Check you're in the right folder
2. Verify all files exist
3. Contact developer

---

## 🎯 Step 1: Start the Server

### Method A: Using Python (Recommended)

**Windows / Mac / Linux:**

1. **Open Terminal/Command Prompt**
   - Windows: `Win + R`, type `cmd`, press Enter
   - Mac: `Cmd + Space`, type `terminal`, press Enter
   - Linux: `Ctrl + Alt + T`

2. **Navigate to frontend folder**
   ```bash
   cd g:\projects\Interview-agent\frontend
   ```

3. **Start the server**
   ```bash
   python -m http.server 8080
   ```

4. **Wait for confirmation**
   ```
   Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
   ```

---

### Method B: Using Node.js (No Installation)

**Windows / Mac / Linux:**

1. **Open Terminal/Command Prompt**

2. **Navigate to frontend folder**
   ```bash
   cd g:\projects\Interview-agent\frontend
   ```

3. **Start the server**
   ```bash
   npx http-server
   ```

4. **Look for output**
   ```
   http://127.0.0.1:8080
   ```

---

### Method C: Direct File (Offline)

1. **Navigate to**: `g:\projects\Interview-agent\frontend\`
2. **Find**: `index.html`
3. **Double-click** to open in browser

*(Limited functionality - use Method A or B for full features)*

---

## 🌐 Step 2: Open in Browser

1. **Once server is running**, open your browser
2. **Type this in address bar**:
   ```
   http://localhost:8080
   ```
3. **Press Enter**

**You should see:**
- Matrix code rain falling in background
- Login form in center
- Dark theme with neon accents
- No errors in browser

---

## 🎮 Step 3: First Test (5 minutes)

### Test 1: View Frontend
```
✓ Open http://localhost:8080
✓ See login page with code rain
✓ See "InterviewPilot" logo
✓ See email/password form
✓ See "Sign up here" link
✓ See animated background
```

### Test 2: Create Account
```
Click: "Sign up here"
Fill:
  - Name: Test User
  - Email: test@example.com
  - Password: Test123!@#
  - Confirm: Test123!@#
Click: "Create Account"

Expected: Redirect to onboarding page
```

### Test 3: Complete Onboarding
```
Select: Role = "Senior Engineer"
Select: Experience = "5-10 years"
Type: Companies = "Google, Meta"
Type: Goals = "Master interviews"
Click: "Continue"

Expected: Redirect to dashboard
```

### Test 4: View Dashboard
```
Expected display:
✓ "Welcome back, Test User" greeting
✓ 4 stat cards (interviews, score, etc.)
✓ Recent interviews list
✓ "Start New Interview" button
✓ "Logout" button in corner
```

**If all 4 tests pass**: ✅ Frontend is working!

---

## 🔧 Step 4: Verify Everything Works

### Open DevTools (F12)

1. **Press `F12`** to open DevTools
2. **Click "Console" tab**
3. **Paste this code** and press Enter:

```javascript
fetch('http://localhost:8001/docs')
  .then(r => console.log('✓ Backend connected'))
  .catch(e => console.error('✗ Backend error:', e))
```

**Expected output:**
```
✓ Backend connected
```

### Check Network Tab

1. **Click "Network" tab** in DevTools
2. **Refresh page** (`Ctrl+R`)
3. **Look for**:
   - All requests show green checkmarks (200 status)
   - No red errors
   - CSS files loading: base.css, components.css, etc.
   - JS files loading: main.js, api-client.js, etc.

**If you see errors:**
- [ ] Backend not running - start it first
- [ ] Wrong URL - check http://localhost:8001
- [ ] Firewall blocking - check Windows Firewall

---

## 🎨 Step 5: Test Core Features

### Test Authentication
```
1. Click "Logout" button
   Expected: Go to login page
   
2. Login with test account
   Email: test@example.com
   Password: Test123!@#
   Expected: Go to dashboard
```

### Test Navigation
```
1. On dashboard, click "Start New Interview"
   Expected: Go to interview page
   
2. See question displayed
   
3. Type answer in textarea
   
4. Click "Next"
   Expected: Next question loads
```

### Test Feedback
```
1. Complete interview (click through all questions)
   
2. Click "End Interview"
   Expected: Feedback page with score
   
3. See score circle and breakdown
   
4. Click "View Readiness Report"
   Expected: Skills report displays
```

---

## 📱 Step 6: Test Mobile (Optional)

1. **Open DevTools** (`F12`)
2. **Click device icon** or press `Ctrl + Shift + M`
3. **Select iPhone 12** from dropdown
4. **Test**:
   - ✓ Layout reorganizes for narrow screen
   - ✓ Buttons still clickable
   - ✓ Text still readable
   - ✓ No horizontal scroll

---

## 🚀 Step 7: You're Done!

**Congratulations!** The frontend is working.

### What to do next:

**Option A: Keep Exploring**
- Try all pages and features
- Test login/logout
- Start interviews
- View feedback
- See readiness report

**Option B: Read Documentation**
- [QUICK_START.md](QUICK_START.md) - 5-minute overview
- [FRONTEND_README.md](FRONTEND_README.md) - Features & design
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Full documentation
- [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) - Comprehensive testing

**Option C: Deploy to Production**
- Use [SETUP_GUIDE.md](SETUP_GUIDE.md) deployment section
- Or run: `vercel` for instant cloud deployment

---

## 🐛 Troubleshooting

### "Cannot connect to server"
```bash
# Check Python installed
python --version

# Check port 8080 not in use
netstat -ano | findstr :8080

# Kill process on port 8080
taskkill /PID <PID> /F

# Try different port
python -m http.server 8081
# Then open http://localhost:8081
```

### "Code rain not showing"
```javascript
// In DevTools Console:
console.log(window.codeRain)

// Should show CodeRain object
// If undefined, check src/js/code-rain.js loaded
```

### "API calls failing"
```bash
# Check backend running
curl http://localhost:8001/docs

# If fails, start backend:
cd backend
python -m uvicorn main:app --port 8001
```

### "Signup/Login not working"
```javascript
// In DevTools Console:
fetch('http://localhost:8001/api/auth/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

### "Mobile layout broken"
```
1. Open DevTools (F12)
2. Click device toggle (Ctrl+Shift+M)
3. Refresh page (Ctrl+R)
4. Check responsive.css loaded
```

---

## 💡 Pro Tips

### TIP 1: Keep DevTools Open
```
While testing, keep DevTools open (F12)
Watch Console for errors
Check Network for API calls
```

### TIP 2: Use Console for Debugging
```javascript
// Check current user
window.auth.getCurrentUser()

// Navigate programmatically
window.router.goTo('/dashboard')

// Control animation
window.codeRain.setSpeed(2)
```

### TIP 3: Clear Cache if Issues
```
Windows: Ctrl + Shift + Delete
Mac: Cmd + Shift + Delete
Then select "All time"
Click "Clear data"
```

### TIP 4: Test Different Browsers
```
Chrome, Firefox, Safari, Edge
Each may render slightly different
Ensures broader compatibility
```

### TIP 5: Check Network Tab
```
F12 → Network tab → Refresh
Look for:
- 200 responses (green) = OK
- 404 responses (red) = Missing files
- 5xx responses = Server error
```

---

## 📊 Expected Results

### After Startup (30 seconds)

```
✓ Terminal shows: "Serving HTTP..."
✓ Browser loads page
✓ Code rain animation visible
✓ Login form displayed
✓ DevTools console clean (no errors)
✓ Network tab shows all 200s
```

### After Signup (1 minute)

```
✓ Form validates input
✓ API call made to backend
✓ User account created
✓ Redirected to onboarding
✓ Onboarding form displays
```

### After Onboarding (2 minutes)

```
✓ Form validates selections
✓ API call to backend
✓ Profile saved
✓ Redirected to dashboard
✓ User stats displayed
```

### After Interview (5 minutes)

```
✓ Questions load
✓ Timer counts down
✓ Answers submitted
✓ Progress updates
✓ Feedback displays with score
✓ Readiness shows skills
```

---

## 🎯 Success Criteria

**Frontend is working correctly if:**

- [x] Loads without 404 errors
- [x] Code rain animation smooth (60fps)
- [x] Forms accept input
- [x] API calls successful
- [x] Pages navigate correctly
- [x] Mobile responsive
- [x] No console errors
- [x] Logout works
- [x] Session persists on refresh
- [x] Performance fast (< 3s load)

---

## 📞 Need Help?

### Quick Questions
```
Where do I start?               → This file (you're reading it!)
How do I run the code?          → Step 1 above
What if something breaks?       → Troubleshooting section
How do I deploy?                → SETUP_GUIDE.md
```

### Detailed Questions
```
Features?                       → FRONTEND_README.md
Setup & config?                 → SETUP_GUIDE.md
How to test?                    → TESTING_CHECKLIST.md
Project status?                 → PROJECT_SUMMARY.md
Common commands?                → COMMAND_REFERENCE.md
```

### During Testing
```
Open DevTools (F12)
Check Console tab for errors
Check Network tab for API calls
Look for 200 responses
Search for error messages
```

---

## 📋 Quick Reference

### URLs to Remember
```
Frontend:    http://localhost:8080
Backend:     http://localhost:8001
API Docs:    http://localhost:8001/docs
```

### Keyboard Shortcuts
```
F12              → Open DevTools
Ctrl+Shift+M     → Toggle mobile view
Ctrl+R           → Refresh page
Ctrl+Shift+R     → Hard refresh
Tab              → Focus next element
Enter            → Submit form
```

### File Locations
```
CSS:             src/css/*.css
JavaScript:      src/js/*.js
Config:          src/js/api-client.js (API URL)
Backend URL:     src/js/api-client.js (line 1)
```

---

## ✅ Final Checklist

Before considering it "working":

- [ ] Backend running on port 8001
- [ ] Frontend server running on port 8080
- [ ] Page loads in browser
- [ ] Code rain animation visible
- [ ] No errors in Console (DevTools)
- [ ] All Network requests = 200
- [ ] Can sign up
- [ ] Can login
- [ ] Can complete onboarding
- [ ] Can start interview
- [ ] Can see feedback
- [ ] Can view readiness report
- [ ] Mobile responsive (Ctrl+Shift+M)
- [ ] Logout works
- [ ] Session persists on refresh

**If all checked**: ✅ **READY FOR PRODUCTION**

---

## 🎉 Congratulations!

You've successfully:

✅ Started the frontend server
✅ Opened it in browser
✅ Verified it works
✅ Tested core features
✅ Checked mobile responsiveness

**You're now ready to:**
- Deploy to production
- Run comprehensive tests
- Gather user feedback
- Iterate and improve

---

## 📞 Next Steps

1. **Read Full Docs**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **Run Tests**: [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)
3. **Deploy**: See SETUP_GUIDE.md → Deployment section
4. **Monitor**: Set up analytics and error tracking

---

**Status**: ✅ **OPERATIONAL**

**Keep this file handy for quick reference!**

---

Last Updated: 2026-01-28 | Version: 1.0.0

