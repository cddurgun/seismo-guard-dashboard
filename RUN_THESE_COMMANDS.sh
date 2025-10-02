#!/bin/bash

# 🚀 SEISMO-GUARD Deployment Commands
# Run these commands in order to deploy your dashboard

echo "🌍 SEISMO-GUARD Deployment Script"
echo "=================================="
echo ""

# Navigate to project directory
cd /Users/turkischleopard/seismo-guard-dashboard

echo "✅ Git repository already initialized and committed!"
echo ""

# Step 1: Authenticate with GitHub
echo "📝 Step 1: Authenticate with GitHub"
echo "Run this command and follow the prompts:"
echo ""
echo "  gh auth login"
echo ""
read -p "Press Enter after you've completed GitHub authentication..."

# Step 2: Create repo and push
echo ""
echo "📤 Step 2: Creating GitHub repository and pushing code..."
echo ""

gh repo create seismo-guard-dashboard \
  --public \
  --description "🌍 SEISMO-GUARD: AI-Powered Earthquake Risk Monitoring Dashboard with real-time data from AFAD, EMSC, and USGS" \
  --source=. \
  --push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Code successfully pushed to GitHub!"
    echo ""

    # Get the repo URL
    REPO_URL=$(gh repo view --json url -q .url)
    echo "📦 Repository: $REPO_URL"
    echo ""
else
    echo "❌ Failed to create repository. Please run manually:"
    echo "   gh repo create seismo-guard-dashboard --public --source=. --push"
    exit 1
fi

# Step 3: Deploy to Railway
echo "🚂 Step 3: Deploy to Railway"
echo ""
echo "Choose your deployment method:"
echo ""
echo "Option A: Web Interface (Recommended for first-time)"
echo "  1. Visit: https://railway.app"
echo "  2. Login with GitHub"
echo "  3. New Project → Deploy from GitHub repo"
echo "  4. Select: seismo-guard-dashboard"
echo "  5. Generate domain in Settings"
echo ""
echo "Option B: Railway CLI"
echo "  Run: npm install -g @railway/cli"
echo "  Then: railway login"
echo "  Then: railway init"
echo "  Then: railway up"
echo ""

read -p "Press Enter to open Railway in browser..."

# Open Railway
open https://railway.app

echo ""
echo "🎉 Deployment Instructions Complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. ✅ Code is on GitHub"
echo "  2. ⏳ Deploy to Railway (follow Option A or B above)"
echo "  3. 🌐 Get your live URL from Railway"
echo "  4. ✨ Share your earthquake monitoring dashboard!"
echo ""
echo "📚 For detailed help, see: DEPLOY_NOW.md"
echo ""
