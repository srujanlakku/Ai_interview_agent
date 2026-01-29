# InterviewPilot Frontend - Complete Setup & Verification Guide

**Comprehensive guide to set up, configure, and verify the production-ready frontend.**

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Development](#development)
6. [Troubleshooting](#troubleshooting)
7. [Architecture](#architecture)
8. [Deployment](#deployment)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **RAM**: 2GB
- **Storage**: 100MB
- **Network**: Internet connection

### Backend Requirements (Running)
- **Service**: http://localhost:8001 (FastAPI)
- **Database**: SQLite initialized
- **Tables**: 8 tables created (users, interviews, etc.)
- **API**: Swagger UI accessible at http://localhost:8001/docs

### Optional: For Development
- **Node.js**: 16.14.0 or higher
- **npm**: 8.0.0 or higher
- **Package**: vite, react, zustand (for React version)

---

## 🔧 Installation

### Step 1: Navigate to Frontend Directory
```bash
cd g:\projects\Interview-agent\frontend
```

### Step 2: Verify Files
Confirm all essential files exist:
```bash
# Windows
dir index.html
dir src\css
dir src\js

# Mac/Linux
ls -la index.html
ls -la src/css/
ls -la src/js/
```

### Step 3: Start Server (Choose One)

#### Option A: Python HTTP Server (No Dependencies)
```bash
cd frontend
python -m http.server 8080
```

#### Option B: Node.js HTTP Server (No Install)
```bash
cd frontend
npx http-server
```

#### Option C: npm with Vite (Full Development)
```bash
cd frontend
npm install
npm run dev
```

#### Option D: Direct File Open
```bash
# Windows
start index.html

# Mac
open index.html

# Linux
xdg-open index.html
```

### Step 4: Open in Browser
```
http://localhost:8080
```
(Adjust port if using different server)

---

## ⚙️ Configuration

### 1. Backend URL Configuration

Edit `src/js/api-client.js`:

```javascript
// Find this section:
const BASE_URL = 'http://localhost:8001';

// Change to your backend URL:
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';
```

### 2. API Timeout Configuration

In `src/js/api-client.js`:

```javascript
const TIMEOUT_MS = 10000;  // 10 seconds
// Change to:
const TIMEOUT_MS = 30000;  // 30 seconds (for slower networks)
```

### 3. Code Rain Speed Configuration

In `src/js/main.js` (DOMContentLoaded):

```javascript
// Find:
window.codeRain = new CodeRain('code-rain-canvas');

// Add after:
window.codeRain.setSpeed(1.5);  // 0.5-3, default 1.5
window.codeRain.setOpacity(0.7); // 0-1, default 0.6
```

### 4. Color Theme Configuration

Edit `src/css/base.css`:

```css
:root {
    /* Primary Colors */
    --color-accent-green: #00ff41;    /* Main accent */
    --color-accent-cyan: #00d4ff;     /* Secondary accent */
    --color-accent-purple: #b000ff;   /* Tertiary accent */
    
    /* Background Colors */
    --color-bg-dark: #0a0e27;         /* Main background */
    --color-bg-darker: #050812;       /* Overlay background */
    --color-bg-light: #1a1f3a;        /* Card background */
}
```

### 5. Typography Configuration

In `src/css/base.css`:

```css
:root {
    --font-primary: 'Orbitron', monospace;
    --font-mono: 'JetBrains Mono', monospace;
}
```

---

## ✅ Verification Checklist

### Step 1: Backend Connectivity Check

```javascript
// Open DevTools Console (F12 → Console tab)

// 1. Test backend health
fetch('http://localhost:8001/docs')
    .then(r => r.text())
    .then(d => console.log('Backend OK'))
    .catch(e => console.error('Backend failed:', e))

// 2. Test API response
fetch('http://localhost:8001/api/auth/health')
    .then(r => r.json())
    .then(d => console.log('API response:', d))
```

### Step 2: Frontend Loading Check

```javascript
// In DevTools Console:

// 1. Check code rain initialized
console.log(window.codeRain)  // Should show CodeRain object

// 2. Check router initialized
console.log(window.router)    // Should show Router object

// 3. Check API client initialized
console.log(window.api)       // Should show APIClient object

// 4. Check auth initialized
console.log(window.auth)      // Should show Auth object
```

### Step 3: CSS Loading Check

```javascript
// In DevTools Console:

// Check all stylesheets loaded
Array.from(document.styleSheets).map(s => s.href)
// Should show 5 CSS files:
// - base.css
// - code-rain.css
// - components.css
// - pages.css
// - responsive.css
```

### Step 4: JavaScript Loading Check

```javascript
// In DevTools Console:

// Check all scripts loaded
Array.from(document.scripts)
    .filter(s => s.src)
    .map(s => s.src)
// Should show 5 JS files:
// - code-rain.js
// - api-client.js
// - router.js
// - auth.js
// - main.js
```

### Step 5: Network Connectivity Check

1. **Open DevTools** → **Network Tab**
2. **Refresh page** (Ctrl+R)
3. **Check results**:
   - [ ] All CSS files: 200 OK
   - [ ] All JS files: 200 OK
   - [ ] No 404 errors
   - [ ] No CORS errors
   - [ ] Initial load < 5 seconds

### Step 6: Animation Check

1. **Look at page background** → Should see Matrix effect
2. **Falling characters** visible
3. **Colors cycling** (green → cyan → purple)
4. **No stuttering** in animation
5. **Animation doesn't block UI** (can still click buttons)

### Step 7: Interactive Elements Check

```javascript
// Test buttons work
document.querySelector('button').click()  // Should work

// Test forms work
document.querySelector('input').focus()   // Should show focus

// Test localStorage
localStorage.setItem('test', 'value')
localStorage.getItem('test')              // Should return 'value'
localStorage.removeItem('test')
```

### Step 8: Page Routing Check

1. **Open DevTools** → **Console**
2. **Navigate to pages**:
   ```javascript
   window.router.goTo('/login')      // ✓ Should show login
   window.router.goTo('/signup')     // ✓ Should show signup
   window.router.goTo('/dashboard')  // ✓ Should redirect to login (not authed)
   ```

### Step 9: Authentication Check

```javascript
// Check auth state
window.auth.isLoggedIn()           // false (not logged in)
window.auth.getCurrentUser()       // null (no user)
window.auth.getToken()             // null (no token)
```

### Step 10: Mobile Responsiveness Check

1. **Open DevTools** → **Device Toolbar** (Ctrl+Shift+M)
2. **Test breakpoints**:
   - [ ] iPhone 12 (390x844): Responsive
   - [ ] iPad (768x1024): 2-column layout
   - [ ] Desktop (1920x1080): Full layout
   - [ ] Landscape mode: Adjusts correctly

---

## 💻 Development

### Project Structure

```
frontend/
├── index.html                 # Entry point
├── src/
│   ├── css/                  # All styles
│   │   ├── base.css          # 1,200+ lines (theme, variables)
│   │   ├── code-rain.css     # 60+ lines (animation)
│   │   ├── components.css    # 1,500+ lines (UI components)
│   │   ├── pages.css         # 800+ lines (page layouts)
│   │   └── responsive.css    # 600+ lines (media queries)
│   └── js/                   # All logic
│       ├── code-rain.js      # 150+ lines (Canvas animation)
│       ├── api-client.js     # 250+ lines (Backend API)
│       ├── router.js         # 80+ lines (SPA routing)
│       ├── auth.js           # 120+ lines (Auth state)
│       └── main.js           # 800+ lines (6 pages + init)
├── public/                   # Static assets
├── QUICK_START.md           # Quick start guide
├── TESTING_CHECKLIST.md     # Test guide
└── SETUP_GUIDE.md           # This file
```

### File Sizes

```
index.html           ~5 KB
src/css/base.css     ~50 KB
src/css/code-rain.css ~1 KB
src/css/components.css ~60 KB
src/css/pages.css    ~40 KB
src/css/responsive.css ~25 KB
---
Total CSS           ~176 KB (minified: ~80 KB)

src/js/code-rain.js  ~8 KB
src/js/api-client.js ~10 KB
src/js/router.js     ~3 KB
src/js/auth.js       ~5 KB
src/js/main.js       ~35 KB
---
Total JS            ~61 KB (minified: ~25 KB)

TOTAL               ~242 KB (minified: ~110 KB)
```

### Adding New Features

#### 1. Add New CSS Component

Create in `src/css/components.css`:
```css
.my-component {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: var(--color-bg-light);
    border: 1px solid var(--color-accent-green);
    border-radius: var(--radius-md);
}

.my-component:hover {
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
}
```

#### 2. Add New Page

Create in `src/js/main.js`:
```javascript
function MyPage() {
    return `
        <div class="my-page-container">
            <h1>My Page</h1>
            <p>Content here</p>
        </div>
    `;
}

// Register in initializePages():
router.register('/mypage', MyPage, false);
```

#### 3. Add Event Listener

In `attachEventListeners()`:
```javascript
const element = document.getElementById('myElement');
if (element) {
    element.addEventListener('click', async () => {
        // Handle click
    });
}
```

---

## 🚨 Troubleshooting

### Issue: "Cannot GET /"

**Cause**: Server not started
**Solution**:
```bash
# Check if running
ps aux | grep python
# or
netstat -ano | findstr :8080

# Start server
python -m http.server 8080
```

### Issue: "Code rain not showing"

**Cause**: Canvas not rendering
**Solution**:
```javascript
// In console:
console.log(document.getElementById('code-rain-canvas'))
console.log(window.codeRain.draw())
```

### Issue: "CORS error"

**Cause**: Backend not allowing requests
**Solution** (Backend fix):
```python
# In FastAPI app:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: "API calls returning 401"

**Cause**: Token invalid or expired
**Solution**:
```javascript
// In console:
localStorage.clear()  // Clear token
window.location.reload()  // Reload
// Login again
```

### Issue: "Mobile layout broken"

**Cause**: Viewport meta missing or CSS not loaded
**Solution**:
```html
<!-- In index.html -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Check CSS loaded -->
<link rel="stylesheet" href="src/css/base.css">
<link rel="stylesheet" href="src/css/responsive.css">
```

### Issue: "Slow performance"

**Cause**: Code rain animation too heavy
**Solution**:
```javascript
// Reduce animation load
window.codeRain.setOpacity(0.3)  // Make more transparent
window.codeRain.setSpeed(0.8)    // Slow down
```

### Issue: "Form not submitting"

**Cause**: JavaScript error or API endpoint wrong
**Solution**:
```javascript
// In console:
console.error()  // Check for errors
// Check endpoint:
fetch('http://localhost:8001/api/auth/login')
```

---

## 🏗️ Architecture

### Component Hierarchy

```
index.html (Entry)
├── Canvas (code-rain-canvas)
│   └── CodeRain animation
├── App Container (#app)
│   ├── LoginPage
│   ├── SignupPage
│   ├── OnboardingPage
│   ├── DashboardPage
│   ├── InterviewPage
│   ├── FeedbackPage
│   └── ReadinessPage
└── Global Scripts
    ├── CodeRain (window.codeRain)
    ├── APIClient (window.api)
    ├── Router (window.router)
    ├── Auth (window.auth)
```

### Data Flow

```
User Input
    ↓
Event Listener (main.js)
    ↓
API Call (api-client.js)
    ↓
Backend Response
    ↓
Auth/Storage (auth.js)
    ↓
Router Navigation (router.js)
    ↓
Page Render (main.js component)
    ↓
CSS Styling (css files)
    ↓
Browser Display
```

### State Management

```
localStorage
├── accessToken    → JWT token
└── user          → User object

window.auth
├── token         → In-memory token
├── user          → In-memory user
└── Methods       → isLoggedIn, login, logout

window.router
├── routes        → Registered routes
├── current       → Current page
└── Methods       → register, navigate, goTo

window.api
├── token         → Current token
└── Methods       → All API endpoints
```

### Authentication Flow

```
1. Signup
   signup() → POST /api/auth/signup → token + user → localStorage → onboarding

2. Login
   login() → POST /api/auth/login → token + user → localStorage → dashboard

3. Protected Route
   access → check auth.isLoggedIn() → if false → redirect /login

4. Logout
   logout() → POST /api/auth/logout → clear localStorage → login page
```

---

## 🚀 Deployment

### 1. Production Build

```bash
# Minify CSS
cd src/css
# Use online CSS minifier or:
npm install -g cssnano
cssnano base.css > base.min.css

# Minify JS
npm install -g terser
terser src/js/main.js -o src/js/main.min.js

# Update index.html to use minified files
```

### 2. Environment Configuration

Create `.env.production`:
```
VITE_API_URL=https://api.interviewpilot.com
VITE_APP_NAME=InterviewPilot
VITE_APP_VERSION=1.0.0
```

### 3. Deploy to Vercel

```bash
npm install -g vercel
vercel
# Follow prompts
```

### 4. Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod --dir=frontend
```

### 5. Deploy to S3 + CloudFront

```bash
# Build
mkdir dist
cp index.html dist/
cp -r src dist/

# Deploy
aws s3 sync dist/ s3://my-bucket/ --delete
aws cloudfront create-invalidation --distribution-id ABC123 --paths "/*"
```

### 6. Docker Deployment

```dockerfile
# dockerfile exists
docker build -t interview-pilot-frontend .
docker run -p 80:80 interview-pilot-frontend
```

---

## 🔐 Security Checklist

- [ ] Remove console.log statements in production
- [ ] Enable HTTPS on backend
- [ ] Set secure cookie flags
- [ ] Validate all user input
- [ ] Sanitize HTML in responses
- [ ] Add rate limiting on backend
- [ ] Implement CSRF tokens
- [ ] Add security headers (CSP, X-Frame-Options)
- [ ] Keep dependencies updated
- [ ] Regular security audits

---

## 📊 Performance Optimization

### Lighthouse Targets

- **Performance**: 90+
- **Accessibility**: 95+
- **Best Practices**: 90+
- **SEO**: 95+

### Optimization Tips

1. **Code Splitting** (if using Vite):
   ```javascript
   import code from './pages/CodePage.js'
   ```

2. **Lazy Load Images**:
   ```html
   <img loading="lazy" src="image.jpg">
   ```

3. **Minify Assets**:
   - CSS: 80 KB → 20 KB
   - JS: 61 KB → 15 KB

4. **Cache Busting**:
   ```html
   <link rel="stylesheet" href="base.css?v=1.0.0">
   ```

---

## 📚 Additional Resources

- **Frontend Repo**: `/frontend/`
- **Quick Start**: `QUICK_START.md`
- **Testing Guide**: `TESTING_CHECKLIST.md`
- **Backend Docs**: http://localhost:8001/docs
- **MDN Web Docs**: https://developer.mozilla.org/

---

## ✅ Final Verification

Before going live:

- [ ] Backend running and healthy
- [ ] All CSS files loading
- [ ] All JS files loading
- [ ] Code rain animation working
- [ ] Forms submitting successfully
- [ ] Pages routing correctly
- [ ] Mobile responsive
- [ ] Accessibility compliance
- [ ] Performance acceptable
- [ ] No console errors

---

**Document Status**: ✅ Complete & Production Ready
**Last Updated**: 2026-01-28
**Version**: 1.0.0

