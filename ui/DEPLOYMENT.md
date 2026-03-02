# Vercel Deployment Guide for Backtesting Engine

There are several ways to deploy your backtesting engine with Vercel. Here are the recommended approaches:

## 🚀 **Option 1: Frontend on Vercel + Backend on Railway/Heroku** (Recommended)

This is the most scalable approach for a Python backend with FastAPI.

### Step 1: Deploy Backend to Railway/Heroku

**Railway (Recommended):**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy backend
cd /home/moew/Documents/BacktestingEngine
railway init
railway up
```

**Or Heroku:**
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create backtesting-engine-api

# Deploy
git push heroku main
```

### Step 2: Deploy Frontend to Vercel

```bash
# Navigate to UI directory
cd /home/moew/Documents/BacktestingEngine/ui

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Project name: backtesting-engine-ui
# - Build command: npm run build
# - Output directory: dist
# - Install command: npm install
```

### Step 3: Update Environment Variables

In Vercel dashboard, add environment variable:
- `VITE_API_URL`: `https://your-railway-backend.railway.app`

---

## 🔧 **Option 2: Full-Stack on Vercel with Edge Functions**

For simpler deployment, but with limitations on Python backend complexity.

### Setup Files Created:
- `vercel.json` - Vercel configuration
- `api/` - Serverless functions directory
- `package-vercel.json` - Simplified package.json

### Deploy Steps:
```bash
cd /home/moew/Documents/BacktestingEngine/ui

# Replace package.json with Vercel version
cp package-vercel.json package.json

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

### Limitations:
- Serverless functions have execution time limits (10s for Hobby, 15s for Pro)
- Memory limitations for complex backtesting
- No persistent storage between function calls

---

## 🎯 **Option 3: Static Frontend with Mock Data**

For demo purposes, deploy just the frontend with mock data.

### Quick Deploy:
```bash
cd /home/moew/Documents/BacktestingEngine/ui

# Update API client to use mock data
# Edit src/lib/api.ts to return mock data instead of API calls

vercel
```

---

## 📋 **Complete Deployment Checklist**

### Prerequisites:
- [ ] GitHub repository with your code
- [ ] Vercel account (free tier available)
- [ ] Railway/Heroku account for backend (if using Option 1)

### Frontend Deployment:
- [ ] Build process works locally (`npm run build`)
- [ ] Environment variables configured
- [ ] API endpoints updated for production URLs
- [ ] CORS configured on backend

### Backend Deployment:
- [ ] Requirements.txt updated
- [ ] Production-ready ASGI server (uvicorn)
- [ ] Environment variables for database/secrets
- [ ] Health check endpoint

### Testing:
- [ ] Test locally with production build
- [ ] Verify API connectivity
- [ ] Check all features work in production
- [ ] Monitor performance and errors

---

## 🚦 **Quick Start Commands**

### Option 1 (Recommended):
```bash
# Deploy backend to Railway
railway login && railway init && railway up

# Deploy frontend to Vercel
cd ui && vercel
```

### Option 2 (Simple):
```bash
# Deploy everything to Vercel
cd ui && vercel
```

### Option 3 (Demo):
```bash
# Deploy static demo
cd ui && npm run build && vercel
```

---

## 🔧 **Environment Variables**

### Frontend (.env):
```
VITE_API_URL=https://your-backend-url.com
VITE_APP_TITLE=Backtesting Engine
```

### Backend:
```
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

## 🌐 **Domain Setup**

Once deployed, you can:
1. Use provided Vercel URLs (e.g., `backtesting-engine.vercel.app`)
2. Connect custom domain in Vercel dashboard
3. Set up SSL (automatic with Vercel)

## 📊 **Monitoring**

Vercel provides:
- Build logs and deployment status
- Function execution logs
- Performance analytics
- Error tracking

Railway/Heroku provide:
- Application logs
- Performance metrics
- Database monitoring