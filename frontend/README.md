# Todo App - Frontend

## Deployment Instructions

### For Vercel Deployment

1. When connecting your project to Vercel, set the **Root Directory** to `frontend`
2. This ensures Vercel recognizes the Next.js project in the frontend directory

### Environment Variables

Set these environment variables in your Vercel project:

- `BACKEND_API_URL`: The URL of your deployed backend (e.g., `https://your-backend.hf.space`)

### Important Notes

- The frontend uses Next.js API routes as a proxy to communicate with the backend
- All API calls from the frontend go through `/api/*` routes which proxy to the backend
- The `BACKEND_API_URL` environment variable determines where the proxy routes forward requests

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server