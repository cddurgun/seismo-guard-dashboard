# SEISMO-GUARD Frontend

This is the frontend static files for the SEISMO-GUARD earthquake monitoring dashboard.

## 🚀 Deploy to Netlify

### Method 1: Drag & Drop (Easiest!)

1. Go to https://app.netlify.com/drop
2. Drag this entire `frontend` folder onto the page
3. Done! ✅

### Method 2: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod
```

### Method 3: GitHub Integration

1. Push this repo to GitHub
2. Go to https://app.netlify.com
3. Click "Add new site" → "Import an existing project"
4. Select your repo
5. Set publish directory: `frontend`
6. Deploy!

## ⚙️ Configuration

After deploying, you need to configure the backend API URL:

**Option A: Edit index.html**
- Open `index.html` line 18
- Set: `window.SEISMO_API_URL = 'https://your-backend-url.com/api';`

**Option B: Browser Console**
- Open your deployed site
- Press F12 (DevTools)
- Console tab:
  ```javascript
  localStorage.setItem('SEISMO_API_URL', 'https://your-backend-url.com/api')
  ```
- Refresh page

## 📁 Files

```
frontend/
├── index.html          # Main dashboard page
├── css/
│   └── styles.css      # Modern glassmorphism styles
└── js/
    └── dashboard.js    # Dashboard logic & API calls
```

## 🔗 Requirements

The frontend needs a backend API running. Deploy the backend to:
- Render: https://render.com
- Railway: https://railway.app
- Fly.io: https://fly.io

See `../DEPLOYMENT_GUIDE.md` for complete instructions.

## 🌐 Live Demo

Once deployed, your dashboard will have:
- ✅ Interactive earthquake map
- ✅ Real-time data charts
- ✅ Risk assessments
- ✅ Pattern detection
- ✅ Mobile responsive design

## 📊 Tech Stack

- **Maps**: Leaflet.js
- **Charts**: Chart.js v4.4.7
- **Styles**: Modern CSS with glassmorphism
- **Icons**: Unicode emoji (no dependencies!)

## 💰 Cost

**FREE!** 🎉
- Netlify free tier: 100GB bandwidth/month
- No build process needed
- Instant deploys
