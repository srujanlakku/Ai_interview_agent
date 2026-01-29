# InterviewPilot Frontend - Testing Guide

Complete checklist for testing all frontend functionality, responsiveness, and integration with backend.

## 🎯 Pre-Testing Checklist

### Backend Status
- [ ] Backend server running on http://localhost:8001
- [ ] Swagger UI accessible at http://localhost:8001/docs
- [ ] Database initialized with tables
- [ ] No API errors in backend logs

### Frontend Status
- [ ] All CSS files present in `src/css/`
- [ ] All JS files present in `src/js/`
- [ ] `index.html` loads without errors
- [ ] No 404s in browser console

### Browser Setup
- [ ] DevTools open (F12) - Console tab active
- [ ] Network tab recording requests
- [ ] Mobile device emulation ready
- [ ] Lighthouse extension installed (optional)

---

## ✅ Phase 1: Visual & Animation Testing

### Code Rain Animation
- [ ] Canvas animation visible on page load
- [ ] Characters falling from top to bottom
- [ ] Colors cycling between green → cyan → purple
- [ ] Animation smooth (60fps, no stuttering)
- [ ] Animation doesn't block UI interactions
- [ ] Animation responsive when window is resized
- [ ] Characters have semi-transparent trails
- [ ] Animation stops on logout
- [ ] Animation restarts on login

### UI Layout Testing
- [ ] Logo renders correctly (green + cyan text)
- [ ] Cards have glassmorphism effect (blur visible)
- [ ] Neon glow effect visible on text elements
- [ ] Buttons have hover effects
- [ ] Buttons have click/active states
- [ ] Progress bars visible and filled correctly
- [ ] Transitions smooth (0.3s)
- [ ] No flickering on page changes

### Colors & Contrast
- [ ] All text readable against dark background
- [ ] WCAG AA contrast ratio met
- [ ] Green accent (#00ff41) prominent
- [ ] Cyan accent (#00d4ff) prominent
- [ ] Dark backgrounds (#0a0e27) consistent
- [ ] No color bleeding at edges

---

## ✅ Phase 2: Authentication Testing

### Signup Flow
1. **Page Load**
   - [ ] Signup page accessible at root URL
   - [ ] Email input focused automatically
   - [ ] All form fields visible
   - [ ] "Already have account? Login" link visible

2. **Form Validation**
   - [ ] Empty form: Cannot submit
   - [ ] Invalid email: Shows error state
   - [ ] Password < 8 chars: Shows helper text
   - [ ] Passwords don't match: Cannot submit
   - [ ] All fields filled: Submit button enabled

3. **API Call**
   - [ ] Click "Create Account" 
   - [ ] Network tab shows POST to `/api/auth/signup`
   - [ ] Request includes: name, email, password
   - [ ] Response 201: Token in response
   - [ ] localStorage updated with token
   - [ ] localStorage updated with user data

4. **Success Flow**
   - [ ] Redirected to `/onboarding` after signup
   - [ ] User name displayed in onboarding
   - [ ] No "Go back" alert triggered

5. **Error Handling**
   - [ ] Duplicate email: Error message displayed
   - [ ] Invalid password format: Error message shown
   - [ ] Network timeout: Graceful error message
   - [ ] 500 server error: Error message shown
   - [ ] Error message persists until corrected

### Login Flow
1. **Page Load**
   - [ ] Login page displayed after logout
   - [ ] Email input focused automatically
   - [ ] Password input visible
   - [ ] "Create account? Sign up" link visible

2. **Form Validation**
   - [ ] Empty form: Cannot submit
   - [ ] Invalid email: Shows error state
   - [ ] All fields filled: Submit button enabled

3. **API Call**
   - [ ] Click "Login"
   - [ ] Network tab shows POST to `/api/auth/login`
   - [ ] Request includes: email, password
   - [ ] Response 200: Token in response
   - [ ] localStorage updated with token

4. **Success Flow**
   - [ ] Redirected to `/dashboard` after login
   - [ ] User greeting displays correct name
   - [ ] Dashboard stats visible
   - [ ] Recent interviews load

5. **Error Handling**
   - [ ] Wrong password: "Invalid credentials" shown
   - [ ] Email not found: Error message shown
   - [ ] Network error: Error handling shown
   - [ ] Error persists until corrected

### Session Persistence
- [ ] Refresh page after login: Still logged in
- [ ] Close tab and reopen: Token still valid
- [ ] localStorage persists across sessions
- [ ] Visit `/login` while logged in: Redirected to `/dashboard`

### Logout
- [ ] Logout button present on dashboard
- [ ] Click logout → API call made
- [ ] POST to `/api/auth/logout` (if backend requires)
- [ ] localStorage cleared after logout
- [ ] Redirected to `/login`
- [ ] Clicking back after logout → cannot go back
- [ ] Cannot access `/dashboard` without token

---

## ✅ Phase 3: Page Navigation Testing

### Page Routing
- [ ] Each page accessible via URL:
  - [ ] `/login` - Login form
  - [ ] `/signup` - Signup form
  - [ ] `/onboarding` - Onboarding form
  - [ ] `/dashboard` - Dashboard
  - [ ] `/interview` - Interview screen
  - [ ] `/feedback` - Feedback page
  - [ ] `/readiness` - Readiness report

### Route Protection
- [ ] Logged-out user cannot access `/dashboard`
- [ ] Logged-out user cannot access `/interview`
- [ ] Logged-out user cannot access `/feedback`
- [ ] Logged-out user cannot access `/readiness`
- [ ] Logged-out user redirected to `/login`
- [ ] Logged-in user cannot access `/login`
- [ ] Logged-in user cannot access `/signup`

### Browser Back/Forward
- [ ] Back button works on all pages
- [ ] Forward button works after back
- [ ] Browser history preserved
- [ ] popstate event triggers correctly

---

## ✅ Phase 4: Onboarding Flow

### Form Fields
- [ ] Role select: All 8 options visible
- [ ] Experience select: All 5 options visible
- [ ] Target companies: Text input accepts multiple
- [ ] Goals: Textarea accepts long text

### Progress Indicator
- [ ] Step 1 highlighted initially
- [ ] Step 2 shows as pending
- [ ] Step 3 shows as pending

### Form Submission
- [ ] All fields required: Cannot submit empty
- [ ] Click "Continue":
  - [ ] Network shows POST to `/api/profile/onboard`
  - [ ] Request includes: role, experience, target_companies, goals
  - [ ] Response 200 received
  - [ ] Redirected to `/dashboard`

### Error Handling
- [ ] Validation error: Message displayed
- [ ] API error: Error message shown
- [ ] Network timeout: Graceful error

### Success State
- [ ] User data stored in localStorage
- [ ] Dashboard loads with user data
- [ ] Profile complete, can start interviews

---

## ✅ Phase 5: Dashboard Testing

### Page Load
- [ ] Dashboard accessible after onboarding
- [ ] Greeting displays: "Welcome back, [Name]"
- [ ] User avatar visible with initials
- [ ] Logout button present and clickable

### Stats Cards
- [ ] 4 stat cards visible (interviews, score, topics, streak)
- [ ] Card titles readable
- [ ] Card values readable
- [ ] Cards have hover effect

### Recent Interviews Section
- [ ] "Recent Interviews" heading visible
- [ ] Interview list displays:
  - [ ] Company name
  - [ ] Role
  - [ ] Date/time
  - [ ] Score badge
- [ ] "Start New Interview" button visible and clickable

### Readiness Widget
- [ ] "Interview Readiness" heading visible
- [ ] Overall score displays (e.g., "82%")
- [ ] Progress bar fills correctly
- [ ] Top areas badges visible
- [ ] "View Full Report" link works

### API Calls
- [ ] GET `/api/profile` (or equivalent) called on load
- [ ] GET `/api/interviews/list` called
- [ ] GET `/api/memory/summary` called
- [ ] All requests return 200

### Responsive Design
- [ ] Stats grid: 4 columns on desktop
- [ ] Stats grid: 2 columns on tablet
- [ ] Stats grid: 1 column on mobile
- [ ] Content remains readable at all sizes

---

## ✅ Phase 6: Interview Screen Testing

### Page Load
- [ ] Interview screen loads after clicking "Start"
- [ ] Question title displays
- [ ] Question number shows (Q1 of 5, etc.)
- [ ] Question type badge visible

### Question Display
- [ ] Question text readable
- [ ] Question description/hints visible
- [ ] Answer textarea present
- [ ] Placeholder text shows
- [ ] Microphone button visible
- [ ] Clear button visible

### Timer Section
- [ ] Timer visible in sidebar
- [ ] Time displays correctly (MM:SS format)
- [ ] Timer countdown working (updates every second)
- [ ] Timer color is cyan
- [ ] Text glow effect visible

### Progress Indicator
- [ ] Progress text shows current question
- [ ] Progress bar fills to current %
- [ ] Progress updates as user moves through interview

### Buttons
- [ ] "Previous" button disabled on first question
- [ ] "Next" button enabled after first question
- [ ] "End Interview" button present
- [ ] All buttons have hover effects

### Form Interaction
- [ ] Type in textarea → text appears
- [ ] Click "Clear" → textarea empties
- [ ] Click "Next" → API call made
- [ ] Submitted answers saved

### API Calls
- [ ] GET `/api/interviews/{id}/questions` on load
- [ ] POST `/api/interviews/{id}/answer` when next clicked
- [ ] All calls return success

### Error States
- [ ] Missing answer: Error shown when trying to next
- [ ] Network error: Graceful handling
- [ ] API timeout: Timeout message shown

---

## ✅ Phase 7: Feedback Page Testing

### Page Load
- [ ] Feedback page accessible after interview
- [ ] "Interview Complete!" heading visible
- [ ] All elements render correctly

### Score Display
- [ ] "Overall Performance" heading visible
- [ ] Score circle displays (e.g., "82/100")
- [ ] Performance badge visible (e.g., "Excellent")
- [ ] Score text is green and glowing

### Detailed Breakdown
- [ ] 4 metrics displayed in grid:
  - [ ] Technical Knowledge (e.g., 85/100)
  - [ ] Communication (e.g., 78/100)
  - [ ] Problem-Solving (e.g., 82/100)
  - [ ] Confidence & Presence (e.g., 80/100)
- [ ] Each metric shows:
  - [ ] Score value
  - [ ] Progress bar (filled to %)
  - [ ] Short description

### Areas for Improvement
- [ ] List displays 3-5 areas
- [ ] Each item readable
- [ ] Recommendations specific and actionable

### Action Buttons
- [ ] "Back to Dashboard" button works
- [ ] "Start Another Interview" button works
- [ ] "View Readiness Report" button works

### API Calls
- [ ] GET `/api/interviews/{id}/feedback` on load
- [ ] Data displays correctly
- [ ] All scores accurate

---

## ✅ Phase 8: Readiness Report Testing

### Page Load
- [ ] Readiness page loads from dashboard
- [ ] "Interview Readiness Report" heading visible
- [ ] Overall score displayed (e.g., "78%")

### Skill Cards
- [ ] 6 skill cards visible in grid:
  - [ ] Algorithms & Data Structures (85%)
  - [ ] System Design (72%)
  - [ ] Behavioral Questions (80%)
  - [ ] Database Design (68%)
  - [ ] API Design (76%)
  - [ ] Communication Skills (81%)
- [ ] Each card shows:
  - [ ] Skill name
  - [ ] Score (%)
  - [ ] Progress bar
  - [ ] Weekly improvement badge (e.g., "+12% this week")

### Recommendations
- [ ] 3 recommendation cards visible:
  - [ ] Emoji icon present
  - [ ] Title and description
  - [ ] Actionable advice
- [ ] Recommendations are personalized to user

### Responsive Layout
- [ ] Cards: 3 columns on desktop
- [ ] Cards: 2 columns on tablet
- [ ] Cards: 1 column on mobile
- [ ] Cards remain readable at all sizes

### API Calls
- [ ] GET `/api/memory/summary` on load
- [ ] GET `/api/memory/strengths` called
- [ ] GET `/api/memory/weaknesses` called
- [ ] All data displays correctly

---

## ✅ Phase 9: Responsive Design Testing

### Desktop (1920x1080)
- [ ] Code rain visible
- [ ] All content visible without scroll
- [ ] Multi-column layouts used
- [ ] Full spacing applied
- [ ] Fonts at full size

### Tablet (768x1024)
- [ ] Code rain visible (scaled appropriately)
- [ ] 2-column layouts collapse to 1 where needed
- [ ] Content still readable
- [ ] Buttons appropriately sized
- [ ] No horizontal scroll

### Mobile (375x812) - iPhone
- [ ] Code rain visible
- [ ] All content single column
- [ ] Buttons full width
- [ ] Button height ≥ 44px
- [ ] Input font size 16px (no iOS zoom)
- [ ] No horizontal scroll
- [ ] Spacing appropriate for small screen

### Small Device (360x640)
- [ ] All content visible
- [ ] Extreme spacing compression
- [ ] Font sizes still readable
- [ ] Buttons remain clickable
- [ ] No layout breaks

### Landscape Mode (1024x600)
- [ ] Layout adapts to narrow height
- [ ] Horizontal scrolling avoided
- [ ] Content not hidden
- [ ] Navigation still accessible

### Device Emulation Testing
- [ ] iPhone 12: All elements visible
- [ ] iPhone SE: No layout breaks
- [ ] iPad Pro: Multi-column layouts used
- [ ] Galaxy S21: Responsive breakpoints work
- [ ] Pixel 5: Touch targets 44x44px minimum

### Touch Testing (if available)
- [ ] All buttons easily tappable
- [ ] No double-tap needed
- [ ] Hover effects ignored on touch
- [ ] Focus states clear and visible
- [ ] No accidental triggers

---

## ✅ Phase 10: Forms Testing

### Login Form
- [ ] Email field: Accepts valid emails only
- [ ] Password field: Masked (dots not visible)
- [ ] Form validates on submit
- [ ] Error messages clear and helpful
- [ ] Tab order: Email → Password → Button
- [ ] Enter key submits form

### Signup Form
- [ ] Name field: Accepts text input
- [ ] Email field: Validates email format
- [ ] Password field: Shows strength indicator (optional)
- [ ] Confirm password: Must match password
- [ ] All fields required
- [ ] Error messages specific
- [ ] Success feedback shown

### Onboarding Form
- [ ] Role select: Dropdown works on all browsers
- [ ] Experience select: Selectable options
- [ ] Companies input: Text input works
- [ ] Goals textarea: Multi-line input works
- [ ] Form validation prevents empty submission
- [ ] Step indicator updates
- [ ] Continue button functional

### Interview Answer Form
- [ ] Textarea accepts long text
- [ ] Auto-expands as user types
- [ ] Clear button empties field
- [ ] Save works when moving to next
- [ ] Previous answers preserved

### All Forms
- [ ] Autocomplete works
- [ ] Spellcheck shows in textareas
- [ ] Copy/paste works
- [ ] Mobile keyboard appropriate for field type:
  - [ ] Email: Shows @
  - [ ] Password: Hides text
  - [ ] Number: Shows numbers
- [ ] No field overflow on mobile

---

## ✅ Phase 11: Error Handling Testing

### Network Errors
- [ ] Disconnect internet → See error message
- [ ] Reconnect internet → Retry works
- [ ] Slow network → Timeout handled gracefully
- [ ] 4xx errors: Specific message shown
- [ ] 5xx errors: Generic message shown

### API Errors
- [ ] 401 Unauthorized: Redirected to login
- [ ] 403 Forbidden: Error message shown
- [ ] 404 Not Found: Error message shown
- [ ] 500 Server Error: Error message shown
- [ ] Network timeout: Error message shown

### Form Errors
- [ ] Invalid email: Error message shown
- [ ] Password too short: Validation message
- [ ] Passwords don't match: Error shown
- [ ] Required field empty: Cannot submit
- [ ] All errors clear when user corrects

### Recovery
- [ ] After error, user can retry
- [ ] After error, user can go back
- [ ] After error, form state preserved
- [ ] No stuck loading states

---

## ✅ Phase 12: Accessibility Testing

### Keyboard Navigation
- [ ] Tab cycles through all interactive elements
- [ ] Shift+Tab reverses tab order
- [ ] Enter activates buttons
- [ ] Enter/Space submits forms
- [ ] Escape closes modals (if any)
- [ ] Focus visible on all elements

### Screen Reader (if available)
- [ ] Page title announced
- [ ] Page structure read correctly
- [ ] Form labels associated with inputs
- [ ] Button purposes clear
- [ ] Error messages announced
- [ ] Success messages announced

### Color Contrast
- [ ] Test with WebAIM Color Contrast Checker
- [ ] Green text (on dark): WCAG AA pass
- [ ] Cyan text (on dark): WCAG AA pass
- [ ] White text (on dark): WCAG AAA pass
- [ ] Button text: WCAG AA minimum

### Focus Indicators
- [ ] Visible focus ring on all buttons
- [ ] Visible focus ring on all inputs
- [ ] Focus not hidden
- [ ] Focus order logical (top to bottom)

### Reduced Motion
- [ ] Code rain animation respects `prefers-reduced-motion`
- [ ] Button animations disabled if requested
- [ ] Transitions disabled if requested
- [ ] Page still functional and readable

---

## ✅ Phase 13: Performance Testing

### Page Load
- [ ] Initial load < 3 seconds
- [ ] Code rain animation starts < 1 second
- [ ] First contentful paint < 1 second
- [ ] DOM content loaded < 2 seconds
- [ ] All resources loaded < 5 seconds

### Network
- [ ] CSS files: < 100KB total
- [ ] JS files: < 100KB total
- [ ] HTML: < 10KB
- [ ] All requests successful (200)
- [ ] No 404s on static assets
- [ ] No duplicate requests

### Runtime Performance
- [ ] 60fps code rain animation (DevTools Frames)
- [ ] No long tasks (> 50ms)
- [ ] Smooth page transitions
- [ ] No jank on form input
- [ ] No memory leaks (DevTools Memory)

### Lighthouse Audit
- [ ] Performance: > 80
- [ ] Accessibility: > 90
- [ ] Best Practices: > 85
- [ ] SEO: > 90

---

## ✅ Phase 14: Browser Compatibility

### Desktop Browsers
- [ ] Chrome 90+: All features work
- [ ] Firefox 88+: All features work
- [ ] Safari 14+: All features work
- [ ] Edge 90+: All features work

### Mobile Browsers
- [ ] Chrome Mobile: All features work
- [ ] Safari iOS: All features work
- [ ] Firefox Mobile: All features work
- [ ] Samsung Internet: All features work

### Feature Support
- [ ] Canvas 2D API: Supported
- [ ] Fetch API: Supported
- [ ] LocalStorage: Supported
- [ ] History API: Supported
- [ ] CSS Grid: Supported
- [ ] CSS Flexbox: Supported
- [ ] CSS Backdrop Filter: Supported
- [ ] CSS Custom Properties: Supported

---

## 🔍 Detailed Test Cases

### Test Case 1: Complete New User Journey
```
1. Open http://localhost:5173
2. See login page with code rain
3. Click "Sign up here"
4. Fill signup form:
   - Name: "John Developer"
   - Email: "john@example.com"
   - Password: "SecurePass123!"
   - Confirm: "SecurePass123!"
5. Click "Create Account"
   ✓ See loading state
   ✓ API call made to /api/auth/signup
   ✓ Redirected to onboarding
6. Fill onboarding:
   - Role: "Senior Engineer"
   - Experience: "5-10 years"
   - Companies: "Google, Meta, Amazon"
   - Goals: "Ace system design interviews"
7. Click "Continue"
   ✓ API call made to /api/profile/onboard
   ✓ Redirected to dashboard
8. See dashboard with stats
   ✓ Greeting shows "Welcome back, John"
   ✓ Stats display correctly
   ✓ Recent interviews list visible
9. Click "Start New Interview"
   ✓ Redirected to interview page
10. Answer question:
    ✓ Question displays
    ✓ Timer counts down
    ✓ Progress shows current question
11. Click "Next"
    ✓ Answer submitted
    ✓ Next question loads
12. Complete all 5 questions
    ✓ "End Interview" becomes active
13. Click "End Interview"
    ✓ Redirected to feedback page
14. See feedback:
    ✓ Score circle shows 82/100
    ✓ Breakdown shows metrics
    ✓ Recommendations show
15. Click "View Readiness Report"
    ✓ Readiness page shows
    ✓ Skills grid displays
    ✓ Recommendations show
16. Click "Back to Dashboard"
    ✓ Back on dashboard
17. Click "Logout"
    ✓ Redirected to login
    ✓ localStorage cleared
    ✓ Cannot access /dashboard
```

### Test Case 2: Returning User
```
1. Open http://localhost:5173/login
2. Enter email: "john@example.com"
3. Enter password: "SecurePass123!"
4. Click "Login"
   ✓ API call to /api/auth/login
   ✓ Token stored in localStorage
   ✓ Redirected to dashboard
5. See dashboard with previous data
   ✓ User greeting shows name
   ✓ Previous interviews show
   ✓ Stats updated
6. Verify token persists:
   ✓ Refresh page (Cmd+R)
   ✓ Still logged in
   ✓ token still in localStorage
```

### Test Case 3: Error Scenarios
```
1. Try invalid login:
   - Email: "test@example.com"
   - Password: "WrongPassword"
   ✓ Error: "Invalid credentials"
   ✓ Form preserved
   ✓ Can retry

2. Try signup with duplicate email:
   - Use previously created email
   ✓ Error: "Email already exists"
   ✓ Can try different email

3. Try network error:
   - Unplug internet during form submit
   ✓ Error: "Network error" or "Timeout"
   ✓ Can reconnect and retry

4. Try accessing protected route without login:
   - Open /dashboard in URL bar
   ✓ Redirected to /login
   ✓ Cannot bypass auth
```

---

## 📊 Test Results Template

```
Test Date: _______________
Tester: _______________
Browser: _______________
Device: _______________
OS: _______________

VISUAL DESIGN
✓ Code rain animation: ___
✓ Glassmorphism: ___
✓ Color scheme: ___
✓ Typography: ___
✓ Spacing: ___

AUTHENTICATION
✓ Signup flow: ___
✓ Login flow: ___
✓ Session persistence: ___
✓ Logout: ___
✓ Auth errors: ___

PAGES
✓ Dashboard: ___
✓ Interview: ___
✓ Feedback: ___
✓ Readiness: ___
✓ Routing: ___

RESPONSIVENESS
✓ Desktop: ___
✓ Tablet: ___
✓ Mobile: ___
✓ Landscape: ___
✓ Touch: ___

FORMS
✓ Validation: ___
✓ Submission: ___
✓ Error handling: ___
✓ Accessibility: ___

API INTEGRATION
✓ Signup request: ___
✓ Login request: ___
✓ Profile request: ___
✓ Interview request: ___
✓ Feedback request: ___

OVERALL SCORE: ___/100

ISSUES FOUND:
1. ___
2. ___
3. ___

NOTES:
_______________
```

---

## 🚀 Final Sign-Off

- [ ] All 14 phases tested
- [ ] No critical issues remain
- [ ] No major issues blocking release
- [ ] Performance acceptable
- [ ] Mobile responsive
- [ ] Accessibility compliant
- [ ] Browser compatibility verified
- [ ] Ready for production deployment

**Status**: ✅ **TESTED & APPROVED** / 🔄 **NEEDS FIXES** / ❌ **BLOCKED**

---

**Document Version**: 1.0
**Last Updated**: 2026-01-28
