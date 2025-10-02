# 🚀 Deploy SEISMO-GUARD Now - Step by Step

✅ Git repository initialized and code committed!
Now let's push to GitHub and deploy to Railway.

---

## Step 1: Authenticate with GitHub (1 minute)

Run this command in your terminal:

```bash
cd /Users/turkischleopard/seismo-guard-dashboard
gh auth login
```

**Follow the prompts:**
1. Select: **GitHub.com**
2. Select: **HTTPS**
3. Select: **Login with a web browser**
4. Press Enter
5. Copy the code shown
6. Browser will open → Paste code → Authorize
7. Done! ✅

---

## Step 2: Create GitHub Repository & Push (30 seconds)

```bash
# Create repo and push (all in one command!)
gh repo create seismo-guard-dashboard --public --source=. --push

# Or if you want it private:
# gh repo create seismo-guard-dashboard --private --source=. --push
```

This will:
- Create `seismo-guard-dashboard` repository on your GitHub
- Push all code automatically
- Set up remote origin

**Your code is now on GitHub!** 🎉

---

## Step 3: Deploy to Railway (2 minutes)

### Option A: Web Interface (Easiest)

1. **Go to**: https://railway.app
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway
4. Click **"New Project"**
5. Click **"Deploy from GitHub repo"**
6. Select **`seismo-guard-dashboard`**
7. Click **"Deploy Now"**
8. Wait ~2 minutes for build
9. Click **"Settings"** → **"Networking"** → **"Generate Domain"**
10. **Your app is live!** 🚀

### Option B: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy
railway up

# Generate domain
railway domain

# Open your app
railway open
```

---

## ✅ Verification

After deployment, your app will be at:
```
https://seismo-guard-dashboard-production.up.railway.app
```

**Check:**
- ✅ Dashboard loads
- ✅ Charts render (3 charts: magnitude, depth, timeline)
- ✅ Map shows earthquake markers
- ✅ API health: `your-url/api/health`
- ✅ API docs: `your-url/docs`

---

## 🎯 Quick Commands Reference

```bash
# Check GitHub repo
gh repo view --web

# View Railway logs
railway logs

# Check Railway status
railway status

# Update deployment (after making changes)
git add .
git commit -m "Update"
git push
# Railway auto-deploys on push!
```

---

## 💡 What Railway Will Do

1. **Detect** Python project
2. **Install** dependencies from `requirements.txt`
3. **Start** FastAPI server on dynamic port
4. **Serve** frontend from `/frontend`
5. **Expose** APIs at `/api/*`
6. **Generate** public URL

**Everything is automatic!** No config needed.

---

## 📊 Expected Resources

**Build time**: ~2 minutes
**Memory**: ~200MB
**Cost**: FREE ($5/month credit, app uses ~$3-4)

---

## 🐛 If Something Goes Wrong

**GitHub auth fails?**
```bash
gh auth logout
gh auth login
```

**Railway build fails?**
- Check Railway logs in dashboard
- Verify `requirements.txt` is committed
- Check Python version (should auto-detect 3.9)

**App not responding?**
- Check Railway logs: `railway logs`
- Verify domain was generated
- First request may take ~30s (cold start)

---

## 🎉 Success!

Once deployed, share your dashboard:
- **Live Dashboard**: `https://your-app.up.railway.app`
- **GitHub Repo**: `https://github.com/YOUR-USERNAME/seismo-guard-dashboard`

---

**Ready? Run the commands above! 🚀**
