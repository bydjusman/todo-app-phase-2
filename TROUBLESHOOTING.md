# Troubleshooting Guide - Login and Signup Issues

## Common Issues and Solutions

### Issue 1: Sign up और Login दोनों काम नहीं कर रहे

**Possible Causes:**
1. Backend server नहीं चल रहा
2. `email-validator` package install नहीं है
3. Database connection issue
4. Port conflict

**Solutions:**

#### Step 1: Backend Dependencies Install करें
```bash
cd backend
pip install email-validator==2.2.0
# या सभी dependencies:
pip install -r requirements.txt
```

#### Step 2: Backend Server Start करें
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Check करें कि server start हो रहा है:
- Terminal में `INFO: Application startup complete` दिखना चाहिए
- Browser में `http://localhost:8000/docs` खोलें - Swagger UI दिखना चाहिए

#### Step 3: Frontend Server Start करें
```bash
cd frontend
npm run dev
```

#### Step 4: Browser Console Check करें
1. Browser में F12 दबाएं
2. Console tab खोलें
3. Network tab खोलें
4. Login/Signup try करें
5. Errors देखें

### Issue 2: "Network error: Unable to connect to the server"

**Solution:**
- Backend server check करें कि चल रहा है
- `http://localhost:8000/api/health` browser में खोलें - response आना चाहिए
- Frontend में `BACKEND_API_URL` environment variable check करें

### Issue 3: "Email already registered" या "Username already registered"

**Solution:**
- Different email/username use करें
- Database reset करें (development में):
  ```bash
  cd backend
  rm test.db  # SQLite database delete करें
  python -m uvicorn app.main:app --reload  # Server restart करें
  ```

### Issue 4: "Invalid email format"

**Solution:**
- Valid email format use करें: `user@example.com`
- Email में spaces नहीं होनी चाहिए
- `@` और `.` जरूरी हैं

### Issue 5: Backend Import Error (EmailStr)

**Solution:**
```bash
cd backend
pip install email-validator==2.2.0
python -m uvicorn app.main:app --reload
```

## Debugging Steps

1. **Backend Logs Check करें:**
   - Terminal में backend server के logs देखें
   - Errors red color में दिखेंगे

2. **Frontend Logs Check करें:**
   - Browser Console (F12) में errors देखें
   - Network tab में failed requests देखें

3. **API Endpoints Test करें:**
   - `http://localhost:8000/docs` - Swagger UI
   - Direct API test करें:
     ```bash
     curl -X POST http://localhost:8000/api/auth/register \
       -H "Content-Type: application/json" \
       -d '{"username":"test","email":"test@example.com","password":"test1234","confirm_password":"test1234"}'
     ```

4. **Database Check करें:**
   - SQLite database file exists check करें: `backend/test.db`
   - Database permissions check करें

## Quick Fix Commands

```bash
# Backend restart
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend restart  
cd frontend
npm run dev

# Database reset (development only)
cd backend
rm test.db
python -m uvicorn app.main:app --reload
```
