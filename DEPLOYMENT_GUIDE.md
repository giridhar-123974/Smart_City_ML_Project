# 🚀 Flask Smart City ML - Deployment Guide

Complete step-by-step guide to deploy your Flask Smart City ML application to production.

## 📋 Table of Contents

1. [Local Deployment](#local-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [Railway App Deployment](#railway-app-deployment)
4. [Render Deployment](#render-deployment)
5. [AWS EC2 Deployment](#aws-ec2-deployment)
6. [Production Checklist](#production-checklist)

---

## Local Deployment

### Option 1: Quickest Way (Batch Script)

**Windows:**
```bash
# Simply double-click or run:
RUN_FLASK.bat
```

**macOS/Linux:**
```bash
bash setup.sh
source venv/bin/activate
python app.py
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create directories
mkdir models logs uploads

# 5. Run the app
python app.py

# 6. Open browser
# Visit: http://localhost:5000
```

### Testing Locally

```bash
# Test signup and login
# 1. Go to http://localhost:5000
# 2. Click "Sign Up"
# 3. Create an account
# 4. Login
# 5. Try traffic prediction

# Test with curl (JSON API)
curl -X POST http://localhost:5000/api/predict/traffic \
  -H "Content-Type: application/json" \
  -d '{
    "hour": 14,
    "day_of_week": 3,
    "vehicle_count": 100,
    "avg_speed": 45,
    "weather": 0
  }'
```

---

## Heroku Deployment

### Step 1: Setup Heroku Account

1. Create account at [heroku.com](https://www.heroku.com/)
2. Install Heroku CLI from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

### Step 2: Prepare Your App

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "initial commit"

# Login to Heroku
heroku login
```

### Step 3: Create Heroku App

```bash
# Create app (replace "smartcity-app" with your app name)
heroku create smartcity-app

# Or if app already exists
heroku git:remote -a smartcity-app
```

### Step 4: Set Environment Variables

```bash
# Set SECRET_KEY
heroku config:set SECRET_KEY="your-super-secret-key-here"

# Set Flask environment
heroku config:set FLASK_ENV="production"

# View all config
heroku config
```

### Step 5: Deploy

```bash
# Push to Heroku
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

### Troubleshooting Heroku

```bash
# Check logs for errors
heroku logs --tail

# Restart app
heroku restart

# Scale dynos
heroku ps:scale web=1

# Check database
heroku config
```

---

## Railway App Deployment

### Step 1: Setup Railway Account

1. Go to [railway.app](https://railway.app/)
2. Sign up with GitHub
3. Authorize access

### Step 2: Connect Repository

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Click "Deploy"

### Step 3: Set Environment Variables

1. Go to Variables tab
2. Add:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - `FLASK_PORT=5000`

### Step 4: Configure Start Command

1. Go to Settings
2. Set **Start Command**: `gunicorn app:app`
3. Save

### Step 5: Deploy

- Railway auto-deploys on push
- Check status in deployments tab
- Visit your app URL

### Railway Monitoring

```bash
# View logs in dashboard
# Railway provides live logs in web interface

# Check memory/CPU usage
# Dashboard shows resource usage
```

---

## Render Deployment

### Step 1: Setup Render Account

1. Go to [render.com](https://render.com/)
2. Sign up with GitHub
3. Connect GitHub account

### Step 2: Create Web Service

1. Dashboard → New → Web Service
2. Connect GitHub repo
3. Select your repository and branch

### Step 3: Configure Service

| Field | Value |
|-------|-------|
| Name | smartcity-ml |
| Runtime | Python 3 |
| Region | Singapore or nearest |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

### Step 4: Set Environment Variables

1. Click Environment
2. Add variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-very-secret-key-here
   ```

### Step 5: Deploy

1. Click "Create Web Service"
2. Render auto-builds and deploys
3. Get your app URL from dashboard
4. Visit: https://your-app.onrender.com

### Monitoring on Render

- Check logs: Logs tab
- Check metrics: Metrics tab
- View deployments: Deployments tab

---

## AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console
2. EC2 → Instances → Launch Instance
3. Select **Ubuntu 22.04 LTS**
4. Instance type: **t2.micro** (free tier eligible)
5. Create security group:
   - Allow SSH (port 22)
   - Allow HTTP (port 80)
   - Allow HTTPS (port 443)
6. Launch instance

### Step 2: Connect to Instance

```bash
# Download .pem file
# Then:
chmod 600 your-key.pem

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git -y

# Clone your repository
git clone https://github.com/your-username/Smart_City_ML_Project.git
cd Smart_City_ML_Project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/smartcity.service
```

**Paste this content:**
```ini
[Unit]
Description=Smart City ML Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Smart_City_ML_Project
ExecStart=/home/ubuntu/Smart_City_ML_Project/venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Save and enable:**
```bash
sudo systemctl start smartcity
sudo systemctl enable smartcity
sudo systemctl status smartcity
```

### Step 5: Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/smartcity
```

**Paste this content:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Enable and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/smartcity /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL Certificate (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew (automatic)
```

### Step 7: Access Your App

- Visit: `http://your-instance-ip`
- Or: `https://your-domain.com` (after SSL setup)

---

## Production Checklist

### Before Going Live

- [ ] Change `SECRET_KEY` in .env to a complex random string
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Test all prediction endpoints
- [ ] Test login/signup flow
- [ ] Verify database migrations
- [ ] Check error logs
- [ ] Enable HTTPS/SSL
- [ ] Setup email notifications (optional)
- [ ] Enable monitoring/alerting

### Environment Variables (Production)

```bash
FLASK_ENV=production
SECRET_KEY=generate-with-: python -c "import secrets; print(secrets.token_hex(32))"
DEBUG=False
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host/dbname  # Use PostgreSQL in production
```

### Performance Optimization

```bash
# Use PostgreSQL instead of SQLite
pip install psycopg2-binary

# Use production server (Gunicorn)
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

# Enable caching
# Add Redis caching layer

# Use CDN for static files
# Cloudflare, AWS CloudFront
```

### Monitoring & Logging

```python
# In production, use:
- Sentry for error tracking
- New Relic for performance monitoring
- ELK Stack for log aggregation
- DataDog for application monitoring
```

### Backup Strategy

```bash
# Backup database daily
# Backup models folder
# Version control on GitHub
# Use database snapshots (AWS RDS, Heroku)
```

---

## Quick Reference

### Local
```bash
python app.py  # http://localhost:5000
```

### Heroku
```bash
heroku create app-name
git push heroku main
```

### Railway
```bash
# Just push to GitHub, Railway auto-deploys
git push origin main
```

### Render
```bash
# Connect GitHub repo in Render dashboard
# Set environment variables
# Deploy
```

### AWS
```bash
ssh -i key.pem ubuntu@ec2-ip
cd Smart_City_ML_Project
source venv/bin/activate
gunicorn app:app
```

---

## Support & Troubleshooting

### Port Already in Use
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Database Errors
```bash
# Reset database
rm smartcity.db
python app.py  # Auto-creates new DB
```

### Models Not Loaded
```bash
# Ensure models/ folder has:
# - traffic_model.pkl
# - air_quality_model.pkl
# - energy_model.pkl

# Or train them:
# jupyter notebook notebooks/
# Run each notebook
```

### 502 Bad Gateway (Nginx)
```bash
# Check Gunicorn logs
sudo journalctl -u smartcity -n 50

# Check Nginx config
sudo nginx -t

# Restart services
sudo systemctl restart smartcity nginx
```

---

## Free Tier Limits

| Platform | Free Tier |
|----------|-----------|
| **Render** | 750 hours/month, auto-sleeps |
| **Railway** | $5/month free credits |
| **Heroku** | Deprecated free tier (2022) |
| **AWS** | 750 hours/month (t2.micro) |

---

## Next Steps

1. **Deploy locally first** ✓
2. **Test all features**
3. **Choose platform** (Render recommended)
4. **Deploy to cloud**
5. **Setup domain name** (optional)
6. **Enable SSL/HTTPS**
7. **Monitor and maintain**

---

**Congratulations! Your Smart City ML App is now live! 🎉**
