# Sign Up aur Login Fix - Step by Step Guide (Urdu/Hindi)

## Problem Kya Hai?
Sign up aur login dono kaam nahi kar rahe.

## Solution - Step by Step

### Step 1: Backend Server Start Karein

**Terminal 1 mein:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Check karein:**
- Terminal mein yeh dikhna chahiye: `INFO: Application startup complete`
- Browser mein `http://localhost:8000/docs` kholen - Swagger UI dikhna chahiye

### Step 2: Frontend Server Start Karein

**Terminal 2 mein (naya terminal):**
```bash
cd frontend
npm run dev
```

**Check karein:**
- Terminal mein yeh dikhna chahiye: `Ready on http://localhost:3000`
- Browser mein `http://localhost:3000` kholen

### Step 3: Dependencies Install Karein (Agar Nahi Kiye)

**Backend dependencies:**
```bash
cd backend
pip install email-validator==2.2.0
pip install -r requirements.txt
```

### Step 4: Browser Console Check Karein

1. Browser mein **F12** dabaen
2. **Console** tab kholen
3. **Network** tab kholen
4. Sign up ya login try karein
5. Errors dekhen

## Common Errors aur Solutions

### Error 1: "Network error: Unable to connect to the server"

**Solution:**
- Backend server check karein - `http://localhost:8000/api/health` browser mein kholen
- Agar response nahi aata, backend server restart karein

### Error 2: "Email already registered"

**Solution:**
- Different email use karein
- Ya database reset karein (development mein):
  ```bash
  cd backend
  rm test.db
  python -m uvicorn app.main:app --reload
  ```

### Error 3: "Invalid email format"

**Solution:**
- Valid email format use karein: `user@example.com`
- Email mein spaces nahi honi chahiye

### Error 4: Backend Server Start Nahi Ho Raha

**Solution:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Agar error aaye, error message share karein.

## Quick Test

**Backend test:**
```bash
# Browser mein:
http://localhost:8000/api/health

# Response aana chahiye:
{"status":"healthy","timestamp":"...","version":"1.0.0"}
```

**Frontend test:**
```bash
# Browser mein:
http://localhost:3000

# Login/Signup page dikhna chahiye
```

## Agar Abhi Bhi Problem Hai

1. **Browser Console (F12)** mein exact error message dekhen
2. **Backend terminal** mein errors dekhen
3. **Network tab** mein failed requests dekhen
4. Error messages share karein

## Important Notes

- **Donon servers** (backend aur frontend) **ek saath** chalne chahiye
- Backend port: **8000**
- Frontend port: **3000**
- Database file: `backend/test.db` (SQLite)
