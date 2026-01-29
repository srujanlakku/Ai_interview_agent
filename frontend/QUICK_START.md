# 🚀 InterviewPilot Frontend - Quick Start Guide

Get the frontend running in **5 minutes**.

---

## 📋 Prerequisites

- Backend server running on `http://localhost:8001`
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Optional: Node.js 16+ (for development server)

---

## ⚡ Quickest Start (No Node.js Required)

### Option 1: Direct Browser
```bash
# Just open the file in your browser
# File → Open File → frontend/index.html
# OR double-click index.html
```

### Option 2: Simple HTTP Server (Python)
```bash
# Navigate to frontend directory
cd frontend

# Start Python server
python -m http.server 8080

# Open browser
http://localhost:8080
```

### Option 3: Node.js HTTP Server
```bash
# Navigate to frontend directory
cd frontend

# Using npx (no install needed)
npx http-server

# Open browser
http://localhost:8080
```

---

## 🎯 What You'll See

1. **Matrix Code Rain**: Falling characters in background
2. **Login Page**: Email + password form
3. **Dark Theme**: Neon green and cyan accents
4. **Glassmorphic UI**: Blurred glass-effect cards

---

## 🧪 First Test Run

### Step 1: Open Frontend
```
Open http://localhost:8080 in browser (or file:// if direct)
```

### Step 2: Verify Backend Connection
```
1. Open DevTools (F12)
2. Go to Console tab
3. Type: fetch('http://localhost:8001/docs')
4. Should see response (not error)
```

### Step 3: Test Signup
```
1. On login page, click "Sign up here"
2. Fill form:
   - Name: Test User
   - Email: test@example.com
   - Password: Test123!@#
   - Confirm: Test123!@#
3. Click "Create Account"
4. Check Network tab (should see POST to localhost:8001)
5. Should redirect to onboarding page
```

### Step 4: Complete Onboarding
```
1. Select role: "Senior Engineer"
2. Select experience: "5-10 years"
3. Enter companies: "Google, Meta"
4. Enter goals: "Master system design"
5. Click "Continue"
6. Should see dashboard
```

### Step 5: Start Interview
```
1. Click "Start New Interview"
2. See interview question
3. Type answer in textarea
4. Click "Next" to proceed
5. Complete interview
6. See feedback score
```

---

## 🔧 Common Issues & Fixes

### "Cannot find backend"
**Problem**: API calls failing, 404 errors
**Fix**: 
- [ ] Verify backend running: `curl http://localhost:8001/docs`
- [ ] Check backend port is 8001 (not different)
- [ ] Check `api-client.js` baseURL is correct

### "Code rain not showing"
**Problem**: No animation in background
**Fix**:
- [ ] Check browser supports Canvas
- [ ] Check z-index (code rain should be behind content)
- [ ] Try refreshing page (Ctrl+R)

### "localStorage not working"
**Problem**: Session lost after refresh
**Fix**:
- [ ] Check browser not in private/incognito mode
- [ ] Open DevTools → Application tab → Clear site data
- [ ] Try different browser

### "Forms not submitting"
**Problem**: Click submit but nothing happens
**Fix**:
- [ ] Open DevTools → Console for errors
- [ ] Check Network tab → see if API call made
- [ ] Verify backend is responding

### "Mobile/tablet not responsive"
**Problem**: Layout broken on small screens
**Fix**:
- [ ] Open DevTools → Toggle device toolbar (Ctrl+Shift+M)
- [ ] Check responsive.css loaded
- [ ] Try portrait orientation

---

## 📁 File Organization

```
frontend/
├── index.html              ← Open this file
├── src/
│   ├── css/
│   │   ├── base.css        ← Theme & variables
│   │   ├── code-rain.css   ← Animation styles
│   │   ├── components.css  ← Button, card styles
│   │   ├── pages.css       ← Page layouts
│   │   └── responsive.css  ← Mobile optimizations
│   └── js/
│       ├── code-rain.js    ← Canvas animation
│       ├── api-client.js   ← Backend API calls
│       ├── router.js       ← Page routing
│       ├── auth.js         ← Auth management
│       └── main.js         ← Page components
├── FRONTEND_README.md      ← Full documentation
├── TESTING_CHECKLIST.md    ← Test guide
└── QUICK_START.md          ← This file
```

---

## 🎨 Customization

### Change Primary Color
Edit `src/css/base.css`:
```css
--color-accent-green: #00ff41;  /* Change to any green */
```

### Change Animation Speed
Edit `src/js/main.js`:
```javascript
codeRain.setSpeed(2);  /* 1-3, where 3 is fastest */
```

### Change Glitch Effect
Edit `src/css/code-rain.css`:
```css
opacity: 0.6;  /* 0-1, lower = more transparent */
```

---

## 🔑 Key Shortcuts

| Action | Shortcut |
|--------|----------|
| Open DevTools | F12 |
| Toggle Mobile View | Ctrl+Shift+M |
| Clear Cache | Ctrl+Shift+Delete |
| Refresh Page | Ctrl+R |
| Hard Refresh | Ctrl+Shift+R |
| Console | Ctrl+Shift+J |
| Network Tab | Ctrl+Shift+E |

---

## 🧩 API Endpoints Used

The frontend calls these endpoints on the backend:

```javascript
// Authentication
POST /api/auth/signup         ← Signup
POST /api/auth/login          ← Login
POST /api/auth/logout         ← Logout

// Profile
POST /api/profile/onboard     ← Complete profile
GET  /api/profile             ← Get user profile

// Interviews
POST /api/interviews          ← Create new
GET  /api/interviews/{id}/questions
POST /api/interviews/{id}/answer
GET  /api/interviews/{id}/feedback

// Memory (stats)
GET  /api/memory/summary      ← Overall stats
GET  /api/memory/strengths    ← Strong areas
GET  /api/memory/weaknesses   ← Weak areas
```

All requests include `Authorization: Bearer <token>` header automatically.

---

## 💾 Local Storage Keys

Browser saves these in localStorage:

```javascript
localStorage.accessToken    // JWT token
localStorage.user          // User object (JSON)
```

To clear:
```javascript
localStorage.clear()
// Or individual:
localStorage.removeItem('accessToken')
localStorage.removeItem('user')
```

---

## 🐛 Debug Mode

To see what's happening:

```javascript
// Open DevTools Console and paste:

// 1. Check auth status
window.auth.isLoggedIn()
window.auth.getCurrentUser()

// 2. Check API connectivity
window.api.healthCheck()

// 3. Check router state
window.router

// 4. Check code rain
window.codeRain.speed
window.codeRain.animate()
```

---

## 📊 Performance Check

```javascript
// In DevTools Console:

// 1. Check load time
performance.timing.loadEventEnd - performance.timing.navigationStart

// 2. Check memory
performance.memory

// 3. Check paint timing
performance.getEntriesByType('paint')
```

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] Update API URL in `src/js/api-client.js`
- [ ] Enable HTTPS on backend
- [ ] Set CORS headers correctly
- [ ] Minify CSS and JS
- [ ] Test all pages
- [ ] Test on mobile
- [ ] Check lighthouse score
- [ ] Set up error tracking
- [ ] Add analytics
- [ ] Create privacy policy
- [ ] Test with real data

---

## 🚀 Production Deploy

### Using Vercel (Easiest)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow prompts
# Your frontend will be live at yourdomain.vercel.app
```

### Using GitHub Pages
```bash
# Create GitHub repo
# Push frontend/ folder to gh-pages branch
# Enable Pages in GitHub settings
# Your frontend will be live at yourusername.github.io/repository
```

### Using Docker
```bash
# Frontend already has Dockerfile
docker build -t interview-pilot-frontend .
docker run -p 8080:80 interview-pilot-frontend
```

---

## 📞 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| White screen | CSS not loading | Check src/css/ files exist |
| No animations | Canvas not supported | Update browser |
| API 401 error | Token invalid | Log out and log back in |
| CORS error | Backend blocking requests | Check backend CORS settings |
| Slow performance | Large animation | Reduce code-rain opacity |
| Mobile broken | Viewport meta missing | Check index.html has <meta viewport> |

---

## 📚 Learning Resources

- [MDN Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [CSS Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [localStorage Docs](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

---

## 🎓 Code Examples

### Add a New Page

1. Create function in `src/js/main.js`:
```javascript
function MyNewPage() {
    return `
        <div class="container">
            <h1>My Page</h1>
            <button id="myButton">Click me</button>
        </div>
    `;
}
```

2. Register in `initializePages()`:
```javascript
router.register('/mypage', MyNewPage, true);  // true = requiresAuth
```

3. Add CSS in `src/css/pages.css`:
```css
.my-page-container {
    display: flex;
    gap: 1rem;
}
```

4. Add event listeners in `attachEventListeners()`:
```javascript
const btn = document.getElementById('myButton');
if (btn) {
    btn.addEventListener('click', () => {
        alert('Clicked!');
    });
}
```

### Make API Call

```javascript
// In any event handler:
const result = await window.api.createInterview('Google', 'Senior', 'hard');
if (result.success) {
    console.log('Interview created:', result.data);
} else {
    console.error('Error:', result.error);
}
```

### Navigate to Page

```javascript
// In any event handler:
window.router.goTo('/dashboard');
```

---

## 🎯 What's Next

1. **Development**: Customize design, add features
2. **Testing**: Run through testing checklist
3. **Deployment**: Deploy to production server
4. **Monitoring**: Set up error tracking & analytics
5. **Iteration**: Collect user feedback, improve

---

## 📞 Support

- **Documentation**: See `FRONTEND_README.md`
- **Testing Guide**: See `TESTING_CHECKLIST.md`
- **Issues**: Check browser console (F12)
- **Backend Issues**: Check backend logs (port 8001)

---

**Status**: ✅ Ready to Run
**Last Updated**: 2026-01-28
**Version**: 1.0.0

