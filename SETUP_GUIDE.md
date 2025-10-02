# 🚀 SEISMO-GUARD Setup Guide

Complete step-by-step instructions for deploying the SEISMO-GUARD earthquake monitoring dashboard.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Docker Deployment](#docker-deployment)
4. [Local Development Setup](#local-development-setup)
5. [Troubleshooting](#troubleshooting)
6. [Production Deployment](#production-deployment)

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows 10+
- **RAM**: 2GB
- **Storage**: 1GB free space
- **Network**: Active internet connection for API access

### Software Requirements

**For Docker Deployment:**
- Docker 20.10+
- Docker Compose 2.0+

**For Local Development:**
- Python 3.11 or higher
- pip 23.0+
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🐳 Docker Deployment (Recommended)

### Step 1: Install Docker

**macOS:**
```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
# Or install via Homebrew
brew install --cask docker
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Add your user to docker group
```

**Windows:**
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Follow installation wizard
- Enable WSL 2 if prompted

### Step 2: Clone/Download Project

```bash
cd ~/Projects  # Or your preferred directory
# If you have git:
git clone <repository-url> seismo-guard-dashboard

# Or download and extract the project files
```

### Step 3: Build and Run

```bash
cd seismo-guard-dashboard

# Build the Docker image
docker-compose build

# Start the container in detached mode
docker-compose up -d

# Check if container is running
docker ps
```

### Step 4: Access Dashboard

Open your web browser and navigate to:
```
http://localhost:8000
```

You should see the SEISMO-GUARD dashboard loading with real-time earthquake data!

### Step 5: Manage Container

```bash
# View logs
docker-compose logs -f

# Stop the container
docker-compose stop

# Start the container
docker-compose start

# Restart the container
docker-compose restart

# Stop and remove container
docker-compose down

# Stop and remove container with volumes
docker-compose down -v
```

---

## 🔧 Local Development Setup

### Step 1: Install Python

**macOS:**
```bash
# Using Homebrew
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip
```

**Windows:**
- Download Python from https://www.python.org/downloads/
- Run installer, check "Add Python to PATH"

### Step 2: Create Virtual Environment

```bash
cd seismo-guard-dashboard

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)`.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 4: Run the Server

```bash
# Navigate to backend directory
cd backend

# Start the FastAPI server
python main.py
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Access Dashboard

Open your browser to:
```
http://localhost:8000
```

### Step 6: Development Workflow

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Testing:**
```bash
# Test API endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/earthquakes/recent
```

**Frontend Development:**
- Edit files in `frontend/` directory
- Refresh browser to see changes
- No build step required for HTML/CSS/JS

---

## 🔍 Troubleshooting

### Issue: Port 8000 Already in Use

**Solution:**
```bash
# Find process using port 8000
# macOS/Linux:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or change port in docker-compose.yml or main.py
```

### Issue: Docker Container Won't Start

**Solution:**
```bash
# Check Docker daemon is running
docker info

# View detailed logs
docker-compose logs

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Issue: API Returns No Data

**Possible Causes:**
1. **No internet connection** - Check your network
2. **AFAD/EMSC APIs down** - The system will use mock data automatically
3. **Firewall blocking** - Allow outbound HTTPS connections

**Debug:**
```bash
# Test API connectivity
curl https://deprem.afad.gov.tr/apiv2/event/filter
curl https://www.seismicportal.eu/fdsnws/event/1/query

# Check backend logs
docker-compose logs seismo-guard
```

### Issue: Frontend Not Loading

**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Clear browser cache
# Chrome: Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)

# Check browser console for errors (F12)
```

### Issue: Python Dependencies Won't Install

**Solution:**
```bash
# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, install individually
pip install fastapi
pip install uvicorn
# ... etc
```

### Issue: Map Not Displaying

**Possible Causes:**
1. **Internet required** - Leaflet loads tiles from CDN
2. **Browser compatibility** - Use modern browser
3. **JavaScript errors** - Check browser console (F12)

---

## 🌐 Production Deployment

### Using Nginx as Reverse Proxy

**1. Install Nginx:**
```bash
# Ubuntu/Debian
sudo apt-get install nginx

# macOS
brew install nginx
```

**2. Configure Nginx:**

Create `/etc/nginx/sites-available/seismo-guard`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**3. Enable and Restart:**
```bash
sudo ln -s /etc/nginx/sites-available/seismo-guard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Systemd Service (Alternative to Docker)

Create `/etc/systemd/system/seismo-guard.service`:
```ini
[Unit]
Description=SEISMO-GUARD Earthquake Monitoring
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/seismo-guard-dashboard/backend
ExecStart=/opt/seismo-guard-dashboard/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable seismo-guard
sudo systemctl start seismo-guard
sudo systemctl status seismo-guard
```

---

## 📊 Monitoring and Maintenance

### Health Check

```bash
# Check API health
curl http://localhost:8000/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-10-02T14:30:00",
  "cache_age_minutes": 2.5
}
```

### Log Management

**Docker logs:**
```bash
# View recent logs
docker-compose logs --tail=100

# Follow logs in real-time
docker-compose logs -f

# Save logs to file
docker-compose logs > seismo-guard.log
```

**Local logs:**
```bash
# Redirect output to log file
python main.py > seismo-guard.log 2>&1
```

### Backup Data

```bash
# Backup data directory
tar -czf seismo-guard-backup-$(date +%Y%m%d).tar.gz data/

# Restore
tar -xzf seismo-guard-backup-20251002.tar.gz
```

---

## 🔐 Security Recommendations

1. **Change default ports** if exposing to internet
2. **Enable HTTPS** with SSL certificate
3. **Use environment variables** for sensitive config
4. **Implement rate limiting** on API endpoints
5. **Regular updates** of dependencies
6. **Monitor logs** for suspicious activity

---

## 📞 Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) for general information
2. Review the [API documentation](#)
3. Open an issue on GitHub
4. Contact support: seismo-guard@example.com

---

## ✅ Post-Installation Checklist

- [ ] Dashboard loads at http://localhost:8000
- [ ] Earthquake map displays with markers
- [ ] Metrics cards show data (events, magnitude, depth)
- [ ] Charts render correctly
- [ ] Risk assessment panel loads
- [ ] Recent events table populates
- [ ] Auto-refresh works (wait 5 minutes)
- [ ] Manual refresh button works
- [ ] Region and magnitude filters work
- [ ] No errors in browser console (F12)

---

**🎉 Congratulations! Your SEISMO-GUARD dashboard is now running!**

Access it anytime at `http://localhost:8000` to monitor seismic activity in Turkey.

**Remember:** This system provides risk assessments, not predictions. Maintain preparedness at all times.

---

© 2025 SEISMO-GUARD | Setup Guide v1.0.0
