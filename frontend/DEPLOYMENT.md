# Todo App Deployment Guide

## Deploying to Vercel

To deploy this application to Vercel, you need to:

1. **Deploy the Backend First**
   - Deploy the FastAPI backend to a cloud platform (Render, Railway, Heroku, etc.)
   - Note the URL of your deployed backend (e.g., `https://your-backend-app.onrender.com/api`)

2. **Configure Vercel Environment Variables**
   After deploying your frontend to Vercel, go to your Vercel project settings and add these environment variables:

   **Environment Variables:**
   - `BACKEND_API_URL`: The URL of your deployed backend (e.g., `https://your-backend-app.onrender.com/api`)
   - `NEXT_PUBLIC_GOOGLE_API_KEY`: Your Google API key (if using Google integration)

3. **Vercel Build Settings**
   - Framework: Next.js
   - Build Command: `npm run build` or leave blank for auto-detection
   - Output Directory: Leave blank (Next.js handles this automatically)

## Local Development

For local development, ensure you have both backend and frontend running:

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## API Proxying

This frontend includes API proxying through Next.js API routes to avoid CORS issues when deployed. All API calls from the frontend are proxied through `/api/*` routes to the actual backend.

## Troubleshooting

If you encounter 404 errors on Vercel:
1. Verify your `BACKEND_API_URL` is set correctly in Vercel environment variables
2. Ensure your backend is deployed and accessible at the configured URL
3. Check that the backend accepts requests from your Vercel deployment domain