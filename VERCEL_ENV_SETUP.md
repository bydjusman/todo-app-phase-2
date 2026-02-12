# Vercel Environment Variables Setup

## Required Environment Variables for Vercel Deployment

Aapko Vercel ke **Environment Variables** section me ye sab variables add karne hain:

### 1. Backend API URL (CRITICAL - Login ke liye zaroori)
```
NEXT_PUBLIC_API_BASE_URL=https://usmannick-todo-app-phase-2.hf.space
```

### 2. Backend API URL (Alternative - Server-side routes ke liye)
```
BACKEND_API_URL=https://usmannick-todo-app-phase-2.hf.space
```

### 3. Legacy Support (Optional - agar kahi use ho raha ho)
```
NEXT_PUBLIC_API_URL=https://usmannick-todo-app-phase-2.hf.space
```

### 4. Google API Key (Agar Google features use kar rahe ho)
```
NEXT_PUBLIC_GOOGLE_API_KEY=AIzaSyDuenkmA70OXn7U6sBTs-uKmbA1IRCyD08
```

---

## Vercel me Kaise Add Karein:

1. Vercel Dashboard me jao
2. Apni project select karo
3. **Settings** → **Environment Variables** me jao
4. Har variable ko **Production**, **Preview**, aur **Development** ke liye add karo
5. Values add karo:
   - `NEXT_PUBLIC_API_BASE_URL` = `https://usmannick-todo-app-phase-2.hf.space`
   - `BACKEND_API_URL` = `https://usmannick-todo-app-phase-2.hf.space`
   - `NEXT_PUBLIC_API_URL` = `https://usmannick-todo-app-phase-2.hf.space` (optional)
   - `NEXT_PUBLIC_GOOGLE_API_KEY` = `AIzaSyDuenkmA70OXn7U6sBTs-uKmbA1IRCyD08` (agar chahiye)

---

## Important Notes:

- ✅ **`NEXT_PUBLIC_*`** variables **client-side** accessible hain (browser me)
- ✅ **`BACKEND_API_URL`** sirf **server-side** routes me use hota hai
- ✅ Sabse zaroori: **`NEXT_PUBLIC_API_BASE_URL`** - ye login/signup ke liye use hota hai
- ⚠️ Variables add karne ke baad **redeploy** karna zaroori hai

---

## Fix Applied:

- `AuthContext.tsx` me `API_URL` ko fix kiya - ab woh `NEXT_PUBLIC_API_BASE_URL` use karega with fallback
- Ab login properly backend ko hit karega Vercel pe bhi

---

## Testing After Deployment:

1. Vercel pe deploy karo
2. Login page kholo
3. Browser DevTools → Network tab me check karo:
   - Login request URL: `https://usmannick-todo-app-phase-2.hf.space/api/auth/login`
   - Method: `POST`
   - Status: 200 ya 401 (not 405)
