# Sign Up aur Login Fix - Quick Guide (Urdu/Hindi)

## Sabse Pehle Ye Karein:

### 1. Backend Server Start Karein

**Terminal/PowerShell mein:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Agar error aaye:**
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 2. Frontend Server Start Karein

**Naya Terminal/PowerShell mein:**
```bash
cd frontend
npm run dev
```

### 3. Browser Mein Test Karein

1. Browser kholen: `http://localhost:3000`
2. **F12** dabaen (Developer Tools)
3. **Console** tab kholen
4. Sign up ya login try karein
5. Errors dekhen

## Agar Backend Start Nahi Ho Raha:

```bash
cd backend
pip install email-validator
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Agar "Network Error" Aaye:

1. Backend server check karein - terminal mein errors dekhen
2. Browser mein yeh URL kholen: `http://localhost:8000/api/health`
3. Agar response nahi aata, backend restart karein

## Agar "Email Already Registered" Aaye:

- Different email use karein
- Ya database delete karein (development only):
  ```bash
  cd backend
  del test.db
  python -m uvicorn app.main:app --reload
  ```

## Important:

- **Donon servers** (backend + frontend) **ek saath** chalne chahiye
- Backend: Port **8000**
- Frontend: Port **3000**

## Test Script Run Karein:

```bash
# Backend test karein:
python test_auth.py
```

Yeh script backend ko test karega aur batayega kya problem hai.
