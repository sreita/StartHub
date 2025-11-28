# Frontend Manual Testing Guide (StartHub)

This document covers 10 key scenarios to validate the frontend against the test backend (port 8081).

- **Backend**: `http://localhost:8081/api/v1`
- **Frontend**: `http://localhost:3000`

---

## Test Scenarios

### 1. Basic Navigation
**Goal**: Verify all pages load without console errors

**Steps**:
- Open `http://localhost:3000/home.html`
- Navigate to `login.html`, `signup.html`, `profile.html`
- Check browser console (F12) for errors

**Expected**: No red errors in console, all pages render correctly

---

### 2. User Registration
**Goal**: Create new user account

**Steps**:
1. Navigate to `signup.html`
2. Fill form with:
   - First Name: `Test`
   - Last Name: `User`
   - Email: `test@example.com`
   - Password: `Password123!`
3. Submit form

**Expected**: 
- Success message appears
- Confirmation email sent (check backend logs)
- User record created in database

---

### 3. User Login
**Goal**: Authenticate and store JWT token

**Steps**:
1. Navigate to `login.html`
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `Password123!`
3. Click "Login"
4. Open DevTools → Application → Local Storage

**Expected**:
- Redirect to `home.html` or `profile.html`
- `localStorage.authToken` contains JWT
- `localStorage.user` contains user JSON

---

### 4. Navbar User Menu
**Goal**: Validate authenticated user interface

**Steps**:
1. After successful login, inspect navbar
2. Verify user menu displays
3. Check for "Logout" option

**Expected**:
- Navbar shows user name/avatar
- Dropdown menu appears on click
- "Logout" button visible

---

### 5. Dark Mode Toggle
**Goal**: Test theme persistence

**Steps**:
1. Click dark mode toggle in navbar
2. Verify UI changes to dark theme
3. Refresh page (F5)
4. Check theme persists

**Expected**:
- Theme switches immediately
- Preference saved to `localStorage`
- Theme persists after page reload

---

### 6. Profile Update
**Goal**: Modify user profile data

**Steps**:
1. Navigate to `profile.html`
2. Verify profile data loads
3. Update fields (e.g., bio, location)
4. Submit form
5. Check DevTools Network tab

**Expected**:
- Current data pre-fills form
- PUT request sent with updated data
- Success response (200 OK)
- UI reflects changes

---

### 7. Password Recovery
**Goal**: Request password reset link

**Steps**:
1. Navigate to `forgot_password.html`
2. Enter registered email: `test@example.com`
3. Submit form
4. Check backend logs for email

**Expected**:
- Success message: "Reset link sent to email"
- Backend logs show email sent
- Reset token generated

---

### 8. Password Reset
**Goal**: Set new password via reset link

**Steps**:
1. Extract reset token from backend logs or email
2. Navigate to `reset_password.html?token=<TOKEN>`
3. Enter new password: `NewPassword123!`
4. Submit form

**Expected**:
- Success message: "Password updated"
- Can login with new password
- Old password no longer works

---

### 9. Route Protection
**Goal**: Validate JWT authentication on protected endpoints

**Steps**:
1. **Without Token**:
   - Clear `localStorage.authToken`
   - Try accessing `GET /startups` via fetch in console
   
2. **With Invalid Token**:
   - Set `localStorage.authToken = "invalid"`
   - Repeat request

3. **With Valid Token**:
   - Login normally
   - Access protected endpoint

**Expected**:
- No token → `401 Unauthorized`
- Invalid token → `403 Forbidden`
- Valid token → `200 OK` with data

---

### 10. Logout
**Goal**: Clear session and return to public view

**Steps**:
1. Click "Logout" in navbar
2. Check DevTools → Application → Local Storage
3. Verify redirect to `home.html`
4. Try accessing `profile.html` directly

**Expected**:
- `authToken` and `user` removed from localStorage
- Redirect to home page
- Navbar shows "Login" button
- Protected pages redirect to login

---

## DevTools Verification Checklist

### Console Tab
- ✅ No red errors during normal operation
- ✅ API responses logged (if debug enabled)
- ⚠️ Yellow warnings acceptable (e.g., 404 for optional CSS)

### Network Tab
- ✅ Registration: `POST /api/v1/registration` → `200 OK`
- ✅ Login: `POST /api/v1/auth/login` → `200 OK` with JWT
- ✅ Protected routes: Include `Authorization: Bearer <token>` header
- ✅ Logout: `POST /api/v1/auth/logout` → `200 OK`

### Application Tab (Local Storage)
- ✅ After login: `authToken` and `user` keys present
- ✅ After logout: Both keys deleted
- ✅ Dark mode: `theme` key persists

---

## Common Issues and Solutions

### CSS 404 Errors
**Issue**: `GET /css/missing.css` → 404  
**Impact**: Low (styling may degrade)  
**Fix**: Verify CSS file paths or add missing files

### CORS Errors
**Issue**: `Access-Control-Allow-Origin` errors  
**Solution**: Use `python scripts/dev-server.py` which enables CORS headers  
**Alternative**: Configure backend CORS for `http://localhost:3000`

### Backend Not Running
**Issue**: `ERR_CONNECTION_REFUSED` on port 8081  
**Solution**:
```bash
cd services/spring-auth
./mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=test
```

### Token Expired
**Issue**: `403 Forbidden` despite having token  
**Cause**: JWT expiration (default: 1 hour)  
**Solution**: Login again to get fresh token

### Database State
**Issue**: User already exists during registration  
**Solution**: Use H2 console at `http://localhost:8081/h2-console` to clear test data  
**Credentials**: JDBC URL `jdbc:h2:mem:testdb`, User `sa`, Password `password`

---

## Automated Test Scripts

### Integration Tests

Run comprehensive integration tests:
```bash
bash scripts/test/test_all_features.sh
```

This script validates:
- **Server Availability**: Spring Boot (8081), FastAPI (8000), Frontend (3000)
- **User Registration**: Creates test user with unique email
- **Email Confirmation**: Extracts and validates confirmation token
- **Authentication**:
  - Successful login with correct credentials
  - Failed login with wrong password
  - Failed login with non-existent user
- **JWT Token**: Validation and extraction
- **Protected Endpoints**: Access with/without valid token
- **Data API** (optional): Health check and database connectivity
- **Frontend** (optional): Page accessibility tests

> 📖 **For complete integration testing details**, see [Integration Testing Guide](INTEGRATION_TESTING.md)

### Python Test Suite

Run comprehensive automated CRUD tests:

**Complete CRUD Test Suite**:
```bash
source .venv/Scripts/activate
python scripts/test/test_crud_complete.py
```

Validates all CRUD operations:
- User registration, profile, authentication, deletion
- Startup CRUD, listing, statistics
- Vote operations with count verification
- Comment CRUD

**Specialized Tests**:
```bash
# Search functionality
python scripts/test/test_search.py

# Votes and comments
python scripts/test/test_votes_comments.py

# Users and startups
python scripts/test/test_users_startups.py

# Quick smoke test
python scripts/test/test_manual.py
```

### Backend Tests

Test all backend services:
```bash
bash scripts/test/test_backend.sh
```

Validates:
- FastAPI CRUD operations (startups, comments, votes)
- Spring Boot authentication endpoints
- Database connectivity for both services
- Service health and availability

### Frontend Tests

Test frontend resources:
```bash
bash scripts/test/test_frontend.sh
```

Validates:
- All HTML pages load (HTTP 200)
- CSS resources accessible
- JavaScript modules load correctly
- API endpoints reachable from frontend

### Running All Tests

```bash
# Start all services
bash scripts/start_all.sh

# Wait for initialization
sleep 10

# Run shell script tests
bash scripts/test/test_backend.sh && \
bash scripts/test/test_frontend.sh && \
bash scripts/test/test_all_features.sh

# Run Python test suites
source .venv/Scripts/activate
python scripts/test/test_crud_complete.py
python scripts/test/test_search.py
```

---

## Manual Testing Checklist

- [ ] All pages load without errors
- [ ] User registration creates account
- [ ] Email confirmation activates account
- [ ] Login stores JWT in localStorage
- [ ] Navbar updates after authentication
- [ ] Dark mode persists after refresh
- [ ] Profile data loads and updates
- [ ] Password recovery sends email
- [ ] Password reset works with valid token
- [ ] Protected routes reject invalid tokens
- [ ] Logout clears session completely

---

## Next Steps

After completing manual tests:
1. Run automated test suite
2. Check backend logs for errors
3. Verify database state in H2 console
4. Test edge cases (invalid inputs, network errors)
5. Document any bugs found

For automated testing details, see `TESTING_GUIDE.md`.