# 🚂 Deploy SEISMO-GUARD to Railway

**One-click deployment for both frontend and backend together!**

---

## ⚡ Quick Deploy (3 Minutes)

### Method 1: GitHub Deployment (Recommended)

1. **Push your code to GitHub** (if not already):
   ```bash
   cd /Users/turkischleopard/seismo-guard-dashboard
   git init
   git add .
   git commit -m "Initial commit - SEISMO-GUARD dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/seismo-guard-dashboard.git
   git push -u origin main
   ```

2. **Deploy to Railway**:
   - Go to https://railway.app
   - Click **"Start a New Project"**
   - Select **"Deploy from GitHub repo"**
   - Authorize Railway to access your GitHub
   - Select your `seismo-guard-dashboard` repository
   - Click **"Deploy Now"**

3. **Railway auto-detects everything!** ✨
   - Detects Python project
   - Installs dependencies from `requirements.txt`
   - Uses the `railway.json` configuration
   - Starts your app automatically

4. **Get your URL**:
   - Click on your deployment
   - Go to **"Settings"** tab
   - Under **"Domains"**, click **"Generate Domain"**
   - Your app is live at: `https://YOUR-APP.up.railway.app`

---

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Or with Homebrew on Mac
brew install railway

# Login
railway login

# Initialize and deploy
cd /Users/turkischleopard/seismo-guard-dashboard
railway init
railway up

# Generate domain
railway domain

# Open your app
railway open
```

---

### Method 3: Direct Git Deploy (No GitHub needed)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
cd /Users/turkischleopard/seismo-guard-dashboard
railway init

# Deploy
railway up

# Generate domain
railway domain
```

---

## 🔧 Configuration

Railway automatically uses these files:
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Start command (backup)

**No additional configuration needed!** Everything is pre-configured.

---

## 🌐 How It Works

Railway will:

1. **Detect Python** → Install Python 3.9
2. **Install dependencies** → `pip install -r requirements.txt`
3. **Start server** → `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. **Serve frontend** → Static files from `/frontend` via FastAPI
5. **Serve API** → All `/api/*` endpoints

**Single URL for everything:**
```
https://your-app.up.railway.app          → Dashboard
https://your-app.up.railway.app/api/health → API Health Check
https://your-app.up.railway.app/docs      → API Documentation
```

---

## ✅ Verification Steps

After deployment, check:

1. **Dashboard loads**: Visit your Railway URL
2. **Charts render**: Check magnitude, depth, and timeline charts
3. **Map shows**: Leaflet map with earthquake markers
4. **API works**: Visit `/api/health` endpoint
5. **No errors**: Check browser console (F12)

---

## 💰 Pricing

**Free Tier:**
- ✅ $5 credit per month
- ✅ Enough for 24/7 uptime of this app
- ✅ No credit card required initially
- ✅ Sleeps after inactivity (wakes in <1 second)

**Estimated usage for SEISMO-GUARD:**
- ~$3-4/month on free tier
- Easily runs 24/7 within free credits

---

## 🎯 Environment Variables (Optional)

If you need to add any environment variables:

1. Go to your Railway project
2. Click **"Variables"** tab
3. Add variables:
   ```
   PYTHON_VERSION=3.9
   ```

Currently, no environment variables are required!

---

## 📊 Monitoring

**Railway Dashboard** shows:
- 📈 CPU and Memory usage
- 📝 Real-time logs
- 🔄 Deployment history
- 🌐 Domain management
- 📊 Usage metrics

**View logs:**
```bash
railway logs
```

---

## 🔄 Updating Your App

### Via Git:
```bash
# Make changes to your code
git add .
git commit -m "Update dashboard"
git push

# Railway auto-deploys on push!
```

### Via CLI:
```bash
railway up
```

---

## 🐛 Troubleshooting

### App not starting?
**Check logs:**
```bash
railway logs
```

**Common issues:**
- Build failed → Check `requirements.txt`
- Port error → Railway sets `$PORT` automatically
- Import errors → Verify all files committed to Git

### Charts not loading?
- Check browser console for errors
- Verify CDN URLs are accessible
- Check API returns data: `/api/earthquakes/recent`

### API returning errors?
- Check logs for Python errors
- Verify backend started successfully
- Check health endpoint: `/api/health`

---

## 🚀 Advanced: Custom Domain

1. Go to your Railway project
2. **Settings** → **Domains**
3. Click **"Custom Domain"**
4. Add your domain: `dashboard.yourdomain.com`
5. Update DNS records as shown:
   ```
   Type: CNAME
   Name: dashboard
   Value: YOUR-APP.up.railway.app
   ```
6. Wait for DNS propagation (5-30 minutes)

---

## 📈 Scaling (If Needed)

Railway automatically handles:
- ✅ Auto-scaling based on traffic
- ✅ Zero-downtime deployments
- ✅ Health checks and restarts
- ✅ HTTPS/SSL certificates

For high traffic, upgrade to paid plan ($20/month for more resources).

---

## 🎓 Railway CLI Commands

```bash
# View status
railway status

# Open dashboard
railway open

# View logs
railway logs

# Link to different project
railway link

# Environment variables
railway variables

# Restart service
railway restart

# Delete project
railway delete
```

---

## 📝 Project Structure

Your Railway deployment serves:

```
/                    → frontend/index.html (Dashboard)
/css/styles.css      → frontend/css/styles.css
/js/dashboard.js     → frontend/js/dashboard.js
/api/*               → FastAPI backend endpoints
/docs                → API documentation (Swagger)
/api/health          → Health check endpoint
```

---

## ✨ Features Enabled

✅ **Frontend**: Modern glassmorphism UI with charts
✅ **Backend**: FastAPI with earthquake data
✅ **APIs**: AFAD, EMSC, USGS data sources
✅ **Maps**: Interactive Leaflet map
✅ **Charts**: Chart.js visualizations
✅ **Auto-refresh**: Every 5 minutes
✅ **Responsive**: Mobile-friendly design

---

## 🎉 You're Done!

Your SEISMO-GUARD dashboard is now live on Railway!

**Share your deployment:**
- Dashboard: `https://your-app.up.railway.app`
- API: `https://your-app.up.railway.app/docs`

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

---

**Happy monitoring! 🌍📊**
