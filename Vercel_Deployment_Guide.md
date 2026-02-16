# Vercel Deployment Guide

## Deploying the Backend to Vercel

### Prerequisites
- A Vercel account
- The Vercel CLI installed (`npm install -g vercel`)

### Step 1: Prepare Backend for Vercel Deployment

1. Make sure your backend has the correct `vercel.json` file:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "index.py"
    }
  ],
  "env": {
    "PYTHONPATH": "$PYTHONPATH:."
  }
}
```

2. Ensure your `requirements.txt` includes all necessary dependencies:
```
fastapi
uvicorn
sqlmodel
python-multipart
bcrypt
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
psycopg2-binary
alembic
```

### Step 2: Deploy the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Deploy to Vercel:
```bash
vercel --prod
```

3. Note the deployment URL (e.g., `https://todo-app-phase-2-backend-git-main-yourname.vercel.app`)

### Step 3: Update Frontend Environment Variables

Once your backend is deployed, you need to update the frontend's environment variables to point to the deployed backend:

1. In your Vercel dashboard for the frontend project, update these environment variables:
```
NEXT_PUBLIC_API_BASE_URL=https://your-deployed-backend-url.vercel.app
BACKEND_API_URL=https://your-deployed-backend-url.vercel.app
```

### Step 4: Deploy the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Deploy to Vercel:
```bash
vercel --prod
```

### Step 5: Configure Environment Variables in Vercel Dashboard

For both backend and frontend deployments, make sure to set the required environment variables in the Vercel dashboard:

#### Backend Environment Variables:
- `DATABASE_URL`: Your PostgreSQL database URL (for production)
- `SECRET_KEY`: A strong secret key for JWT tokens
- Any other environment variables required by your backend

#### Frontend Environment Variables:
- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend
- `BETTER_AUTH_SECRET`: Same as the backend's SECRET_KEY

## Troubleshooting Authentication Issues

If you're still experiencing username/password authentication issues after deployment:

1. **Check the Network Tab**: Open browser developer tools, go to the Network tab, and try logging in. Check the request URL and response.

2. **Verify Backend Endpoint**: Make sure the backend authentication endpoint is accessible:
   ```
   GET /api/v1/auth/login
   POST /api/v1/auth/login
   ```

3. **Check CORS Settings**: Ensure your backend allows requests from your frontend domain.

4. **Verify Environment Variables**: Make sure both frontend and backend have the correct environment variables set in Vercel.

## Testing the Authentication

After deployment, you can test the authentication endpoints:

- Health check: `GET https://your-backend-url.vercel.app/api/v1/health`
- Login: `POST https://your-backend-url.vercel.app/api/v1/auth/login`
- Register: `POST https://your-backend-url.vercel.app/api/v1/auth/signup`

The authentication should work once both the frontend and backend are properly deployed and configured with the correct URLs.