# 🚀 SEISMO-GUARD Deployment Guide

Complete guide to deploy the SEISMO-GUARD earthquake monitoring dashboard to production.

## 📋 Deployment Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   Netlify       │ ───────▶│  Render/Railway  │
│   (Frontend)    │  HTTPS  │    (Backend)     │
│  Static Files   │ ◀─────── │   FastAPI API    │
└─────────────────┘         └──────────────────┘
```

**Why this setup?**
- **Netlify**: Best for static frontends (HTML/CSS/JS), free tier, global CDN
- **Render/Railway**: Free Python hosting for the FastAPI backend

---

## 🎯 Quick Start (Recommended: Netlify + Render)

### Step 1: Deploy Backend to Render

1. **Create a Render account**: https://render.com

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository or use "Public Git repository"
   - Repository URL: Your GitHub repo URL

3. **Configure the service**:
   ```
   Name:           seismo-guard-api
   Environment:    Python 3
   Build Command:  pip install -r requirements.txt
   Start Command:  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   Plan:           Free
   ```

4. **Add Environment Variable**:
   - Key: `PYTHON_VERSION`
   - Value: `3.9`

5. **Deploy**: Click "Create Web Service"

6. **Copy your backend URL**:
   - Example: `https://seismo-guard-api.onrender.com`
   - Save this - you'll need it for the frontend!

---

### Step 2: Deploy Frontend to Netlify

1. **Create a Netlify account**: https://netlify.com

2. **Deploy via Drag & Drop** (Easiest):
   - Go to https://app.netlify.com/drop
   - Drag the entire `frontend` folder onto the page
   - Netlify will deploy it instantly!

3. **OR Deploy via Git**:
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub and select your repository
   - Configure:
     ```
     Base directory:   (leave empty)
     Build command:    (leave empty)
     Publish directory: frontend
     ```

4. **Update API URL**:
   - After deployment, open your site
   - Edit `frontend/index.html` line 18:
   ```javascript
   window.SEISMO_API_URL = 'https://seismo-guard-api.onrender.com/api';
   ```
   Replace with YOUR Render backend URL from Step 1

5. **Re-deploy** (if using drag & drop, just drag again)

6. **Your site is live!** 🎉
   - Example: `https://seismo-guard.netlify.app`

---

## 🔧 Alternative Deployment Options

### Option A: Railway (Backend Alternative)

1. **Go to**: https://railway.app
2. **New Project** → "Deploy from GitHub repo"
3. **Settings**:
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - No build command needed
4. **Deploy**: Railway auto-detects Python and installs dependencies
5. **Get URL**: Click on your service → Settings → Domain

### Option B: Fly.io (Backend Alternative)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
cd seismo-guard-dashboard
fly launch

# Follow prompts, it will auto-detect Python
```

### Option C: All-in-One on Vercel

Vercel can host both, but requires Vercel Serverless Functions setup (more complex).

---

## 🔐 Important Configuration

### Update CORS (if you get CORS errors)

Edit `backend/main.py` line 24-29 to add your Netlify domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # For development
        "https://seismo-guard.netlify.app",  # Add your Netlify URL
        "https://your-custom-domain.com"      # Add custom domain if you have one
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎨 Custom Domain Setup

### For Netlify (Frontend):
1. Go to Site Settings → Domain management
2. Add custom domain
3. Follow DNS setup instructions

### For Render (Backend):
1. Go to your service → Settings
2. Add custom domain under "Custom Domains"
3. Update DNS records as instructed

---

## ✅ Verification Checklist

After deployment, verify everything works:

- [ ] Frontend loads at Netlify URL
- [ ] Dashboard displays without errors
- [ ] Map loads and shows earthquake markers
- [ ] All three charts render correctly
- [ ] Recent events table populates
- [ ] Risk assessment panel shows data
- [ ] Browser console shows no CORS errors
- [ ] Backend health check works: `https://YOUR-BACKEND-URL/api/health`

---

## 🐛 Troubleshooting

### Charts not showing?
- Check browser console for errors
- Verify Chart.js CDN is loading
- Check API endpoint returns data

### CORS Errors?
```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS
```
**Fix**: Update CORS settings in `backend/main.py` (see above)

### Backend not starting on Render?
- Check Render logs
- Verify `requirements.txt` has all dependencies
- Ensure start command is correct: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### API returning 404?
- Verify backend URL is correct
- Check `frontend/index.html` line 18 has correct API URL
- Make sure backend deployed successfully

---

## 📊 Monitoring

### Render:
- View logs in dashboard
- Free tier: spins down after 15 min inactivity (first request may be slow)

### Netlify:
- Analytics available in dashboard
- Deployment logs show build/deploy status

---

## 💰 Cost Breakdown

All FREE for basic usage! 🎉

| Service | Plan | Limits |
|---------|------|--------|
| Netlify | Free | 100GB bandwidth/month, 300 build minutes |
| Render  | Free | Spins down after 15min inactivity |
| Railway | Free | $5 credit/month (enough for 24/7 small app) |

**Recommendation**: Start with Netlify + Render (completely free)

---

## 🔄 Updating Your Deployment

### Update Frontend:
1. Make changes to files in `frontend/`
2. Drag & drop to Netlify again, OR
3. Git push (if connected to repo)

### Update Backend:
1. Make changes to files in `backend/`
2. Git push to your repository
3. Render/Railway auto-deploys on push

---

## 📝 Environment Variables

If you need to configure the backend with environment variables:

**Render/Railway Dashboard**:
- Go to Environment Variables section
- Add as needed (e.g., API keys if using real earthquake APIs)

Currently the app works with mock data, so no env vars needed initially.

---

## 🌐 Full Production Example

**Example deployment**:
- Frontend: `https://seismo-guard.netlify.app`
- Backend: `https://seismo-guard-api.onrender.com`
- API Docs: `https://seismo-guard-api.onrender.com/docs`

---

## 🎓 Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Netlify
3. ✅ Update API URL in frontend
4. ✅ Test everything works
5. 🎨 (Optional) Add custom domain
6. 📈 (Optional) Set up monitoring/analytics

---

## 🆘 Need Help?

Common issues and solutions:

1. **"Failed to fetch"** → Check backend URL is correct
2. **CORS errors** → Update CORS in backend
3. **Charts not loading** → Check browser console for CDN errors
4. **Backend timeout** → First request may be slow on free tier (cold start)

---

## 📄 Summary

Your deployment setup:

```bash
# Files created for deployment:
├── netlify.toml          # Netlify configuration
├── render.yaml           # Render configuration
├── railway.json          # Railway configuration
├── Procfile              # Generic web service config
└── DEPLOYMENT_GUIDE.md   # This file
```

**Everything is ready to deploy!** Just follow the steps above. 🚀

---

✅ **You're all set to deploy SEISMO-GUARD to production!**
