# 🎯 Frontend Command Reference Card

**Quick reference for common frontend tasks and commands.**

---

## 🚀 Starting the Frontend

### Option 1: Python (Most Common)
```bash
cd frontend
python -m http.server 8080
# Browser: http://localhost:8080
```

### Option 2: Node.js (No Install)
```bash
cd frontend
npx http-server
# Browser: http://localhost:8080
```

### Option 3: Direct File (Offline)
```bash
# Windows: Double-click index.html
# Mac: open index.html
# Linux: xdg-open index.html
```

### Option 4: npm (Full Dev)
```bash
cd frontend
npm install
npm run dev
# Browser: http://localhost:5173
```

---

## 🔍 Debugging Commands

### In DevTools Console (F12)

**Check Backend Connection**
```javascript
fetch('http://localhost:8001/docs')
  .then(r => console.log('✓ Backend connected'))
  .catch(e => console.error('✗ Backend error'))
```

**Check Frontend Status**
```javascript
// Is user logged in?
window.auth.isLoggedIn()  // true/false

// Get current user
window.auth.getCurrentUser()  // { name, email, ... }

// Get auth token
window.auth.getToken()  // JWT token string

// Check API client
window.api.healthCheck()  // Test API connectivity
```

**Navigation**
```javascript
// Go to page
window.router.goTo('/dashboard')
window.router.goTo('/interview')
window.router.goTo('/login')

// View all routes
console.log(window.router.routes)
```

**Code Rain Animation**
```javascript
// Control animation
window.codeRain.start()
window.codeRain.stop()
window.codeRain.setSpeed(1.5)    // 0.5-3
window.codeRain.setOpacity(0.7)  // 0-1
```

**Clear Session**
```javascript
localStorage.clear()
location.reload()
// Or logout
window.router.goTo('/login')
```

---

## 📁 File Structure Quick View

```
frontend/
├── 📄 index.html              # Open this file
├── 📁 src/
│   ├── 📁 css/
│   │   ├── base.css           # Theme & colors
│   │   ├── code-rain.css      # Animation
│   │   ├── components.css     # Buttons, cards, etc.
│   │   ├── pages.css          # Page layouts
│   │   └── responsive.css     # Mobile styles
│   └── 📁 js/
│       ├── code-rain.js       # Animation logic
│       ├── api-client.js      # API calls
│       ├── router.js          # Page navigation
│       ├── auth.js            # Login/logout
│       └── main.js            # Page content
├── 📖 README.md              # Start here
├── 📖 QUICK_START.md         # 5-min guide
├── 📖 SETUP_GUIDE.md         # Full setup
├── 📖 TESTING_CHECKLIST.md   # Test cases
└── 📖 PROJECT_SUMMARY.md     # Status
```

---

## 🎨 CSS Customization

### Change Primary Color
File: `src/css/base.css`
```css
:root {
    --color-accent-green: #00ff41;  /* Change this */
}
```

### Change Dark Background
File: `src/css/base.css`
```css
:root {
    --color-bg-dark: #0a0e27;  /* Change this */
}
```

### Change Animation Speed
File: `src/js/main.js`
```javascript
// Find DOMContentLoaded handler:
window.codeRain.setSpeed(1.5)  // Change from 1.5 to your value
```

### Change Animation Opacity
File: `src/js/main.js`
```javascript
window.codeRain.setOpacity(0.7)  // Change from 0.7 to your value
```

---

## 📊 API Endpoints Reference

All requests go through `window.api`:

### Auth
```javascript
await api.signup(email, password, name)
await api.login(email, password)
await api.logout()
```

### Profile
```javascript
await api.onboardUser({
    role: 'Senior Engineer',
    experience: '5-10 years',
    target_companies: 'Google, Meta',
    goals: 'Master interviews'
})
```

### Interviews
```javascript
await api.createInterview(company, role, difficulty)
await api.getInterviewQuestions(interviewId)
await api.submitAnswer(interviewId, questionId, answer)
await api.finalizeInterview(interviewId)
```

### Memory/Stats
```javascript
await api.getMemorySummary()
await api.getStrengths()
await api.getWeaknesses()
```

---

## 🧪 Quick Testing

### Test Signup Flow
```
1. Open http://localhost:8080
2. Click "Sign up here"
3. Fill form:
   Name: Test User
   Email: test@example.com
   Password: Test123!@#
   Confirm: Test123!@#
4. Click "Create Account"
5. Should redirect to onboarding
```

### Test Login Flow
```
1. Open http://localhost:8080/login
2. Enter email: test@example.com
3. Enter password: Test123!@#
4. Click "Login"
5. Should redirect to dashboard
```

### Test Interview Flow
```
1. On dashboard, click "Start New Interview"
2. Type answer in textarea
3. Click "Next" - should advance
4. Click "End Interview" - should go to feedback
5. See score and breakdown
```

---

## 🐛 Common Issues & Fixes

### White screen on load
```
Fix: Check browser console (F12)
- Look for red error messages
- Check if CSS files loading (Network tab)
- Verify index.html opening correctly
```

### API calls failing (401 error)
```
Fix: Token issue
window.localStorage.clear()  // Clear token
location.reload()            // Refresh page
// Login again
```

### Code rain animation stuttering
```
Fix: Reduce animation load
window.codeRain.setOpacity(0.3)  // More transparent
window.codeRain.setSpeed(0.8)    // Slower
```

### Mobile layout broken
```
Fix: Check viewport meta
- Open DevTools (F12 → Toggle device)
- Select mobile device
- Refresh page (Ctrl+R)
- Check responsive.css loaded
```

### Backend not responding
```
Fix: Start backend
# Terminal 1: Stop backend if running
Ctrl+C

# Terminal 2: Start backend
cd backend
python -m uvicorn main:app --reload --port 8001
```

---

## 📈 Performance Check

### In DevTools Console
```javascript
// Load time
performance.timing.loadEventEnd - performance.timing.navigationStart

// Memory usage
performance.memory

// Paint timing
performance.getEntriesByType('paint')

// All resources
performance.getEntriesByType('resource')
```

### Lighthouse Audit (DevTools)
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Click "Generate report"
4. Check scores:
   - Performance: 90+
   - Accessibility: 95+
   - Best Practices: 90+
   - SEO: 95+

---

## 🔑 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| F12 | Open DevTools |
| Ctrl+Shift+M | Toggle mobile view |
| Ctrl+R | Refresh page |
| Ctrl+Shift+R | Hard refresh (clear cache) |
| Ctrl+Shift+J | Open Console |
| Ctrl+Shift+E | Open Network tab |
| Ctrl+Shift+I | Inspect element |
| Tab | Focus next element |
| Shift+Tab | Focus previous element |
| Enter | Activate button/submit form |

---

## 📱 Mobile Testing

### Browser DevTools
```
1. Open DevTools (F12)
2. Click device icon or Ctrl+Shift+M
3. Select device:
   - iPhone 12: 390x844
   - iPhone SE: 375x667
   - iPad: 768x1024
   - Pixel 5: 393x851
```

### Test on Real Device
```
Same network:
http://192.168.1.XXX:8080  (use your IP)

Different network:
Deploy to web and use public URL
```

### Touch Testing
- Tap buttons (should be 44x44px minimum)
- Scroll page (should be smooth)
- Pinch zoom (should work)
- Long press (optional)

---

## 🚀 Deployment Quick Steps

### Deploy to Vercel
```bash
npm install -g vercel
cd frontend
vercel
# Follow prompts
# Live at: https://your-app.vercel.app
```

### Deploy to Netlify
```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod --dir=.
# Follow prompts
# Live at: https://your-app.netlify.app
```

### Deploy to GitHub Pages
```bash
# Push to gh-pages branch
git checkout -b gh-pages
git push origin gh-pages

# Enable in GitHub Settings
# Live at: https://username.github.io/repo
```

---

## 📞 Getting Help

| Question | Answer |
|----------|--------|
| How do I start? | Run `python -m http.server 8080` |
| How do I debug? | Open DevTools (F12) → Console |
| Where's the code? | `src/css/` and `src/js/` |
| How do I customize? | Edit CSS in `src/css/base.css` |
| How do I deploy? | See "Deployment Quick Steps" |
| Where's the docs? | `README.md` or `QUICK_START.md` |
| Is it working? | See code rain animation |
| How do I test? | Check `TESTING_CHECKLIST.md` |

---

## 📊 Page Status Quick Check

### Run This Script
```javascript
// Copy-paste into Console to check all pages

Promise.all([
  (async () => {
    console.log('🔐 Auth:', window.auth.isLoggedIn() ? 'Logged in' : 'Not logged in');
  })(),
  (async () => {
    const result = await window.api.healthCheck();
    console.log('🌐 Backend:', result.success ? 'Connected' : 'Disconnected');
  })(),
  (async () => {
    console.log('🎬 Animation:', window.codeRain ? 'Loaded' : 'Not loaded');
  })(),
  (async () => {
    console.log('📱 Mobile:', window.innerWidth < 768 ? 'Yes' : 'No');
  })(),
  (async () => {
    console.log('🎨 CSS Files:', document.styleSheets.length);
  })(),
  (async () => {
    console.log('📄 Pages:', Object.keys(window.router.routes).length);
  })()
]).then(() => console.log('✅ Check complete!'));
```

---

## 🎯 Daily Checklist

Before pushing to production:

- [ ] Frontend loads without errors
- [ ] Code rain animation visible
- [ ] Login page works
- [ ] Signup form works
- [ ] Dashboard displays
- [ ] Interview page loads
- [ ] No console errors (F12)
- [ ] Mobile responsive (Ctrl+Shift+M)
- [ ] Backend connected
- [ ] All API calls successful
- [ ] Performance good (Lighthouse 90+)
- [ ] Forms validate correctly

---

## 💾 Storage Reference

### localStorage Keys
```javascript
localStorage.accessToken  // JWT token
localStorage.user        // User object (JSON)

// View all
Object.keys(localStorage)

// Clear all
localStorage.clear()

// Clear one
localStorage.removeItem('accessToken')
```

### sessionStorage (optional)
```javascript
sessionStorage.setItem('key', 'value')
sessionStorage.getItem('key')
sessionStorage.clear()
```

---

## 🔗 Quick Links

- **Local Frontend**: http://localhost:8080
- **Backend Docs**: http://localhost:8001/docs
- **Backend Health**: http://localhost:8001/api/health
- **MDN Docs**: https://developer.mozilla.org/
- **CSS Tricks**: https://css-tricks.com/

---

**Print this card for your desk!** 🖨️

---

Last Updated: 2026-01-28 | Version: 1.0.0

