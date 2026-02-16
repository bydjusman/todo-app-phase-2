# Fixing Vercel "Failed to fetch" Error

## Problem
After successful signup on Vercel, you're getting a "Failed to fetch" error when trying to perform other operations (like adding tasks). This happens because:

1. The frontend has proxy API routes in `frontend/src/app/api/[...slug]/route.ts`
2. These proxy routes forward requests to a backend API
3. The backend URL is configured via environment variables
4. The environment variables in Vercel are pointing to an incorrect or non-existent backend

## Solution

### Step 1: Deploy the Backend to Vercel
Make sure your backend is deployed to Vercel and note the deployment URL.

### Step 2: Update Vercel Environment Variables
In your Vercel dashboard for the frontend project, update these environment variables:

```
BACKEND_API_URL=your-actual-backend-url
NEXT_PUBLIC_API_URL=your-actual-backend-url  
NEXT_PUBLIC_API_BASE_URL=your-actual-backend-url
```

For example:
```
BACKEND_API_URL=https://your-backend-project-name.vercel.app
NEXT_PUBLIC_API_URL=https://your-backend-project-name.vercel.app
NEXT_PUBLIC_API_BASE_URL=https://your-backend-project-name.vercel.app
```

### Step 3: Alternative - If Backend is Running Elsewhere
If your backend is running on a different platform (like Hugging Face Spaces, Railway, etc.), use that URL instead:

```
BACKEND_API_URL=https://your-backend-app-name.platform-name.com
NEXT_PUBLIC_API_URL=https://your-backend-app-name.platform-name.com
NEXT_PUBLIC_API_BASE_URL=https://your-backend-app-name.platform-name.com
```

### Step 4: Redeploy Frontend
After updating the environment variables, redeploy your frontend on Vercel for the changes to take effect.

## Verification
After updating the environment variables and redeploying:

1. Visit your Vercel frontend URL
2. Sign up or log in
3. Try adding a task - it should work without the "Failed to fetch" error

## Troubleshooting
If you still have issues:

1. Check browser console for specific error messages
2. Check Network tab to see which URL the requests are going to
3. Verify that your backend is accessible at the configured URL
4. Make sure CORS is properly configured in your backend