# InterviewPilot Frontend

Advanced, production-ready frontend UI for the AI-powered interview platform with Matrix-style code rain effect.

## 🎨 Features

### Visual Design
- ✅ Matrix-style "code rain" falling characters animation (Canvas 2D)
- ✅ Dark theme with neon green (#00ff41) and cyan (#00d4ff) accents
- ✅ Glassmorphism UI cards with backdrop blur effects
- ✅ Smooth animations and transitions
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Touch-friendly interface
- ✅ High-DPI screen optimization

### Technical Features
- ✅ Single-page application (SPA) routing
- ✅ Client-side authentication with JWT tokens
- ✅ API integration with backend
- ✅ Form validation and error handling
- ✅ Local storage for session persistence
- ✅ Keyboard accessibility
- ✅ Prefers-reduced-motion support

## 📁 File Structure

```
frontend/
├── index.html                 # Main HTML entry point
├── src/
│   ├── css/
│   │   ├── base.css          # Core styles, typography, variables
│   │   ├── code-rain.css     # Canvas animation styles
│   │   ├── components.css    # Reusable UI components
│   │   ├── pages.css         # Page-specific layouts
│   │   └── responsive.css    # Media queries & responsiveness
│   ├── js/
│   │   ├── code-rain.js      # Canvas animation logic
│   │   ├── api-client.js     # HTTP client for backend API
│   │   ├── router.js         # SPA routing system
│   │   ├── auth.js           # Authentication state management
│   │   └── main.js           # Page components & initialization
│   ├── components/           # Reusable component templates
│   ├── pages/                # Individual page logic (optional)
│   └── assets/              # Images, fonts, icons
└── public/                   # Static files
```

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Node.js 16+ (optional, for local development server)
- Python backend running on http://localhost:8001

### Installation

1. **No build needed** - Pure HTML/CSS/JavaScript
2. Simply open `index.html` in your browser, or
3. Serve with a local HTTP server:

```bash
# Using Python 3
python -m http.server 8080

# Using Node.js
npx http-server

# Using PHP
php -S localhost:8080
```

Then visit: `http://localhost:8080`

## 📄 Pages

### 1. Login Page (`/login`)
- Email and password input
- Form validation
- Error messages
- Link to signup

### 2. Signup Page (`/signup`)
- Full name, email, password input
- Password confirmation
- Password strength helper
- Link to login

### 3. Onboarding Page (`/onboarding`)
- Target role selection
- Years of experience
- Target companies
- Goals textarea
- Progress indicator

### 4. Dashboard (`/dashboard`)
- User greeting with avatar
- Statistics cards (interviews, score, topics, streak)
- Recent interviews list
- Interview readiness gauge
- Quick action buttons

### 5. Interview Screen (`/interview`)
- Question display
- Answer textarea with audio recording option
- Timer with countdown
- Progress indicator
- Previous/Next navigation
- Tips sidebar
- End interview button

### 6. Feedback/Results (`/feedback`)
- Overall score visualization (circular gauge)
- Performance breakdown by category
- Progress bar for each metric
- Area recommendations
- Navigation buttons

### 7. Readiness Report (`/readiness`)
- Overall readiness score
- 6-category skill breakdown
- Week-over-week improvement badges
- Personalized recommendations
- Practice suggestions

## 🎨 Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Green | #00ff41 | Accents, highlights, success |
| Secondary Cyan | #00d4ff | Secondary highlights, info |
| Purple | #b000ff | Tertiary accent |
| Pink/Red | #ff006e | Error, danger states |
| Warning | #ffd60a | Warning states |
| Dark BG | #0a0e27 | Main background |
| Darker BG | #050812 | Overlay background |
| Light BG | #1a1f3a | Card background |
| Text Primary | #e0e0e0 | Main text |
| Text Secondary | #a0a0a0 | Secondary text |
| Text Muted | #707070 | Disabled/muted text |

### Typography

- **Primary Font**: Orbitron (futuristic tech look)
- **Monospace Font**: JetBrains Mono (code, data display)

### Spacing Scale

```
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
2xl: 3rem (48px)
3xl: 4rem (64px)
```

### Border Radius

```
sm: 0.25rem (4px)
md: 0.5rem (8px)
lg: 1rem (16px)
xl: 1.5rem (24px)
```

## 🧬 Code Rain Animation

The code-rain animation runs continuously in the background using HTML5 Canvas.

### How It Works

1. **Canvas Setup**: Full-screen canvas element positioned behind app content
2. **Character Rain**: Falls from top to bottom using column-based system
3. **Colors**: Cycles through green, cyan, and purple with varying opacity
4. **Fade Effect**: Characters become more transparent as they fall
5. **Performance**: Uses semi-transparent background for trail effect
6. **Responsive**: Automatically resizes with window

### Key Properties

```javascript
const codeRain = new CodeRain();
codeRain.start();           // Start animation
codeRain.stop();            // Stop animation
codeRain.setSpeed(2);       // Set speed (0.5-3)
codeRain.setOpacity(0.6);   // Set opacity (0-1)
```

### Characters Included

- Binary: `0 1`
- Japanese: ア カ キ ク etc.
- ASCII: Various symbols and operators
- Programming: `":<>[]{}()|!@#$%^&*`

## 🔐 Authentication Flow

### 1. Signup
```
User enters email/password → POST /api/auth/signup → Token returned → Onboarding
```

### 2. Login
```
User enters email/password → POST /api/auth/login → Token returned → Dashboard
```

### 3. Protected Routes
```
Token validated → Route accessible
Token missing/invalid → Redirect to login
```

### 4. Token Storage
```
localStorage.setItem('accessToken', token)
localStorage.setItem('user', JSON.stringify(user))
```

## 🎯 Component Library

### Buttons

```html
<!-- Primary (gradient neon) -->
<button class="btn btn-primary">Submit</button>

<!-- Secondary (outlined) -->
<button class="btn btn-secondary">Cancel</button>

<!-- Danger (red outline) -->
<button class="btn btn-danger">Delete</button>

<!-- Sizes -->
<button class="btn btn-sm">Small</button>
<button class="btn btn-lg">Large</button>
```

### Forms

```html
<div class="form-group">
    <label for="input" class="form-label">Label</label>
    <input type="email" class="form-input" placeholder="Enter value">
    <p class="form-helper">Helper text</p>
</div>
```

### Cards

```html
<div class="card">
    <h3>Card Title</h3>
    <p>Card content</p>
</div>

<!-- With accent border -->
<div class="card card-accent">Accent card</div>
```

### Badges

```html
<span class="badge">Default</span>
<span class="badge badge-cyan">Cyan</span>
<span class="badge badge-error">Error</span>
<span class="badge badge-warning">Warning</span>
```

### Progress Bars

```html
<div class="progress-bar">
    <div class="progress-bar-fill" style="width: 75%;"></div>
</div>
```

### Alerts

```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-error">Error message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-info">Info message</div>
```

## 📱 Responsive Breakpoints

- **Desktop**: 769px and up
- **Tablet**: 481px - 768px
- **Mobile**: 360px - 480px
- **Small**: Under 360px
- **Landscape**: Special handling for landscape mode

### Mobile-First Features

- Touch-friendly button sizes (min 44x44px)
- Font size 16px in inputs (prevents zoom on iOS)
- Full-width forms on mobile
- Single-column layouts
- Larger tap targets
- Optimized spacing

## ♿ Accessibility

- ✅ Semantic HTML structure
- ✅ ARIA labels where needed
- ✅ Keyboard navigation support
- ✅ Focus indicators on interactive elements
- ✅ Color contrast compliance (WCAG AA)
- ✅ Reduced motion support
- ✅ Form validation messages

## ⚡ Performance Optimizations

- ✅ CSS animations use GPU (transform, opacity)
- ✅ Canvas animation optimized with requestAnimationFrame
- ✅ Minimal reflows/repaints
- ✅ Efficient event listeners
- ✅ Local storage caching
- ✅ No external dependencies
- ✅ <100KB total (HTML + CSS + JS)

## 🔌 API Integration

All API calls go through the `APIClient` class:

```javascript
// Available methods
await api.signup(email, password, name);
await api.login(email, password);
await api.logout();
await api.getCurrentUser();
await api.createInterview(company, role, difficulty);
await api.getInterviewQuestions(interviewId);
await api.submitAnswer(interviewId, questionId, answer);
await api.finalizeInterview(interviewId);
await api.getMemorySummary();
await api.healthCheck();
```

## 🛠️ Development

### Styling Changes
- Edit files in `src/css/`
- Changes reflect immediately in browser
- No build step needed

### Adding New Pages
1. Create component function in `main.js`
2. Register with router: `router.register('/path', Component, requiresAuth)`
3. Add CSS to `pages.css` if needed

### Debugging
- Open browser DevTools (F12)
- Check Console for errors
- Check Network tab for API calls
- Check Application tab for localStorage

## 🚀 Production Deployment

1. **Update API URL**: Change `baseURL` in `api-client.js`
2. **Enable HTTPS**: Ensure backend is on HTTPS
3. **CORS Settings**: Backend should allow frontend domain
4. **Environment Variables**: Use API key from environment
5. **Cache Busting**: Add version query to CSS/JS imports
6. **Minification**: Minify CSS and JS files
7. **Service Worker**: Optional PWA support

## 🐛 Troubleshooting

### API Connection Issues
- Check backend is running on port 8001
- Check CORS headers in backend
- Check token in localStorage

### Code Rain Not Showing
- Check browser supports Canvas
- Check canvas width/height is set
- Check z-index stacking order

### Form Submission Issues
- Check browser console for errors
- Verify form IDs match in JS
- Check API endpoint is correct

## 📚 Resources

- **Canvas API**: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- **Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **CSS Grid**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout
- **Flexbox**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout

## 📄 License

Proprietary - InterviewPilot Platform

---

**Status**: ✅ Production Ready
**Browser Support**: Chrome, Firefox, Safari 12+, Edge 79+
**Last Updated**: 2026-01-28
