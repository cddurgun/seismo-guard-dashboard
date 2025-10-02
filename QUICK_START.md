# ⚡ SEISMO-GUARD Quick Start Guide

Get your earthquake monitoring dashboard running in **under 2 minutes**!

---

## 🚀 Option 1: Docker (Easiest)

### One Command Startup

```bash
cd ~/seismo-guard-dashboard
./run.sh
```

**That's it!** The script handles everything automatically.

### Or Manually

```bash
# Start the dashboard
docker-compose up -d

# Wait 15 seconds, then open browser to:
# http://localhost:8000

# View logs (optional)
docker-compose logs -f
```

### Stop the Dashboard

```bash
docker-compose stop
```

---

## 🐍 Option 2: Python (Alternative)

```bash
cd ~/seismo-guard-dashboard

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
cd backend
python main.py
```

**Open browser to:** `http://localhost:8000`

---

## 📊 What You'll See

### Real-Time Dashboard Features:

1. **🗺️ Interactive Map**
   - Live earthquake markers
   - Color-coded by magnitude
   - Fault line overlays
   - Click markers for details

2. **📈 Charts & Metrics**
   - Total events (24h)
   - Maximum magnitude
   - Depth distribution
   - 7-day timeline

3. **⚠️ Risk Assessment**
   - Istanbul risk level
   - Confidence scores
   - Probability forecasts
   - Safety recommendations

4. **🔍 Pattern Detection**
   - Seismic sequences
   - Spatial clusters
   - Anomaly alerts

5. **📋 Recent Events Table**
   - Latest significant earthquakes
   - Sortable and filterable

---

## 🔧 Quick Commands

### Docker Commands

```bash
# Start dashboard
docker-compose up -d

# Stop dashboard
docker-compose stop

# Restart dashboard
docker-compose restart

# View logs
docker-compose logs -f

# Stop and remove
docker-compose down
```

### Python Commands

```bash
# Activate environment
source venv/bin/activate

# Run server
python backend/main.py

# Stop server
Ctrl+C
```

### Testing API

```bash
# Health check
curl http://localhost:8000/api/health

# Get recent earthquakes
curl http://localhost:8000/api/earthquakes/recent

# Get Istanbul risk assessment
curl http://localhost:8000/api/risk-assessment/Istanbul
```

---

## 🎯 Dashboard Controls

### Map Filters
- **Region Filter**: Select Istanbul, Marmara, Aegean, etc.
- **Magnitude Filter**: Show only M≥2.0, M≥3.0, M≥4.0

### Auto-Refresh
- Dashboard updates every **5 minutes** automatically
- Click **⟳ Refresh** button for manual update

### Interactive Elements
- **Click earthquake markers** for detailed popup
- **Hover over charts** to see exact values
- **Scroll recent events table** for full history

---

## ⚙️ Configuration (Optional)

### Change Port

**Docker:** Edit `docker-compose.yml`
```yaml
ports:
  - "9000:8000"  # Use port 9000 instead
```

**Python:** Edit `backend/main.py`
```python
uvicorn.run(app, host="0.0.0.0", port=9000)
```

### Adjust Auto-Refresh

Edit `frontend/js/dashboard.js`:
```javascript
const AUTO_REFRESH_INTERVAL = 180000; // 3 minutes (in milliseconds)
```

---

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Then kill the process
kill -9 <PID>
```

### Dashboard Won't Load

1. **Check if server is running:**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Check Docker logs:**
   ```bash
   docker-compose logs
   ```

3. **Clear browser cache** (Ctrl+Shift+Delete)

4. **Try different browser** (Chrome, Firefox, Safari)

### No Data Showing

- **Check internet connection** (APIs need access)
- **Wait 30 seconds** for initial data load
- **Check browser console** (F12) for errors
- The system has **mock data fallback** if APIs are unreachable

---

## 📱 Accessing from Other Devices

### On Same Network

Find your computer's IP address:
```bash
# macOS/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

Then access from other devices:
```
http://YOUR_IP_ADDRESS:8000
```

Example: `http://192.168.1.100:8000`

---

## 📚 Next Steps

### Learn More
- Read **README.md** for complete documentation
- Check **SETUP_GUIDE.md** for advanced setup
- See **PROJECT_SUMMARY.md** for technical details

### Customize
- Edit `frontend/index.html` for layout changes
- Modify `frontend/css/styles.css` for styling
- Update `frontend/js/dashboard.js` for functionality

### Deploy to Production
- See SETUP_GUIDE.md section "Production Deployment"
- Configure Nginx reverse proxy
- Enable HTTPS with Let's Encrypt

---

## ✅ Verification Checklist

After starting, verify:

- [ ] Dashboard loads at http://localhost:8000
- [ ] Map shows Turkey with earthquake markers
- [ ] Metrics cards display numbers
- [ ] Charts render (magnitude, depth, timeline)
- [ ] Risk assessment panel shows data
- [ ] Recent events table has entries
- [ ] No errors in browser console (F12)
- [ ] Manual refresh button works

**If all checked:** ✅ **Your dashboard is ready!**

---

## 🆘 Need Help?

1. **Check SETUP_GUIDE.md** for detailed troubleshooting
2. **View logs** with `docker-compose logs -f`
3. **Test API** with `curl http://localhost:8000/api/health`
4. **Open browser console** (F12) to see JavaScript errors

---

## 🎉 You're All Set!

Your SEISMO-GUARD dashboard is now monitoring earthquake activity in Turkey.

**Remember:**
- 🔄 Auto-refreshes every 5 minutes
- 🚨 Istanbul is HIGH risk zone
- 📊 Data from AFAD + EMSC
- ⚠️ Risk assessments, NOT predictions

**Stay informed. Stay prepared. Stay safe.**

---

### Quick Access

**Dashboard:** http://localhost:8000
**API Health:** http://localhost:8000/api/health
**API Docs:** http://localhost:8000/docs (Swagger UI)

---

© 2025 SEISMO-GUARD | Quick Start Guide v1.0.0
