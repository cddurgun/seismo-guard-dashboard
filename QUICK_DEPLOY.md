# ⚡ Quick Deploy - SEISMO-GUARD

## 🚀 Deploy in 5 Minutes

### Step 1️⃣: Deploy Backend (2 min)

**Using Render** (Recommended - 100% Free):

1. Go to https://render.com/deploy
2. Create account (free)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repo OR paste repo URL
5. Settings:
   - **Name**: `seismo-guard-api`
   - **Environment**: `Python 3`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. Click **"Create Web Service"**
7. **Copy your URL**: `https://seismo-guard-api-XXXX.onrender.com`

---

### Step 2️⃣: Deploy Frontend (2 min)

**Using Netlify** (Recommended - 100% Free):

1. Go to https://app.netlify.com/drop
2. **Drag and drop** the `frontend` folder
3. Done! Your site is live!

**Or use GitHub**:
1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect GitHub and select repo
4. Settings:
   - **Publish directory**: `frontend`
   - Leave everything else empty
5. Click **"Deploy"**

---

### Step 3️⃣: Connect Them (1 min)

1. Open your Netlify site
2. In the browser, open DevTools (F12)
3. Go to **Console** tab
4. Type:
   ```javascript
   localStorage.setItem('SEISMO_API_URL', 'https://YOUR-RENDER-URL.onrender.com/api')
   ```
   Replace with your actual Render URL from Step 1

5. Refresh the page

**OR edit the file**:
- Open `frontend/index.html` line 18
- Change to: `window.SEISMO_API_URL = 'https://YOUR-RENDER-URL.onrender.com/api';`
- Re-upload to Netlify

---

## ✅ You're Done!

Your dashboard is now live at:
- **Frontend**: `https://YOUR-SITE.netlify.app`
- **Backend**: `https://YOUR-API.onrender.com`
- **API Docs**: `https://YOUR-API.onrender.com/docs`

---

## 🎯 Alternative: One-Click Deploy

### Render:
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Railway:
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

### Vercel (Advanced):
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

---

## 🔧 Configuration Files

All deployment configs are ready:
- ✅ `netlify.toml` - Netlify config
- ✅ `render.yaml` - Render config
- ✅ `railway.json` - Railway config
- ✅ `Procfile` - Generic config

Just push to Git and services will auto-detect!

---

## 💡 Tips

**Free Tier Limits**:
- Render: Server sleeps after 15min (first request ~30s to wake)
- Netlify: 100GB bandwidth/month
- Both: Perfect for demos and personal projects!

**Speed up cold starts**:
- Use UptimeRobot or similar to ping your Render URL every 10min

---

See **DEPLOYMENT_GUIDE.md** for detailed instructions!
