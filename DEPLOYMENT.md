# Deployment and Setup Guides

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Configuration](#production-configuration)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.10+
- Git
- Virtual Environment (venv or conda)

### Step-by-Step

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Smart_City_ML_Project.git
cd Smart_City_ML_Project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train ML models
python train_models.py

# 6. Run API server (Terminal 1)
cd Smart_City_ML_Project
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 7. Run Streamlit Dashboard (Terminal 2)
cd Smart_City_ML_Project
streamlit run dashboard/app.py

# 8. Access the application
# API Docs: http://localhost:8000/api/docs
# Dashboard: http://localhost:8501
```

---

## Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Navigate to project directory
cd Smart_City_ML_Project

# Build and start all services
docker-compose up --build

# In another terminal, check service health
docker-compose ps

# View logs
docker-compose logs -f api
docker-compose logs -f dashboard

# Stop services
docker-compose down

# Cleanup volumes
docker-compose down -v
```

### Option 2: Individual Docker Containers

```bash
# Build API image
docker build -f Dockerfile -t smart-city-api:latest .

# Build Dashboard image
docker build -f Dockerfile.dashboard -t smart-city-dashboard:latest .

# Run API
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/datasets:/app/datasets \
  --name smart-city-api \
  smart-city-api:latest

# Run Dashboard
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/datasets:/app/datasets \
  --name smart-city-dashboard \
  smart-city-dashboard:latest

# Check status
docker ps

# View logs
docker logs -f smart-city-api
docker logs -f smart-city-dashboard

# Stop containers
docker stop smart-city-api smart-city-dashboard
docker rm smart-city-api smart-city-dashboard
```

---

## Cloud Deployment

### Heroku Deployment

```bash
# 1. Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login to Heroku
heroku login

# 3. Create Heroku app
heroku create your-app-name

# 4. Add buildpacks
heroku buildpacks:add heroku/python

# 5. Set environment variables
heroku config:set API_DEBUG=False
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set LOG_LEVEL=INFO

# 6. Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 7. Deploy
git push heroku main

# 8. View logs
heroku logs --tail

# 9. Access application
# https://your-app-name.herokuapp.com/api/docs
```

### AWS EC2 Deployment

```bash
# 1. Launch EC2 instance (Ubuntu 22.04 LTS recommended)

# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Update system
sudo apt update && sudo apt upgrade -y

# 4. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 5. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 6. Clone repository
git clone https://github.com/yourusername/Smart_City_ML_Project.git
cd Smart_City_ML_Project

# 7. Create .env file
cat > .env << EOF
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False
LOG_LEVEL=INFO
EOF

# 8. Start services
docker-compose up -d

# 9. Configure security group
# Allow inbound traffic on ports 80, 443, 8000, 8501

# 10. Access application
# http://your-instance-ip:8000/api/docs
# http://your-instance-ip:8501
```

### Azure App Service Deployment

```bash
# 1. Create resource group
az group create --name smartcity-rg --location eastus

# 2. Create container registry
az acr create --resource-group smartcity-rg \
  --name smartcityregistry --sku Basic

# 3. Login to registry
az acr login --name smartcityregistry

# 4. Build and push images
docker build -f Dockerfile -t smartcity-api:latest .
docker tag smartcity-api:latest smartcityregistry.azurecr.io/smartcity-api:latest
docker push smartcityregistry.azurecr.io/smartcity-api:latest

# 5. Create App Service Plan
az appservice plan create --name smartcity-plan \
  --resource-group smartcity-rg --sku B1 --is-linux

# 6. Create Web App
az webapp create --resource-group smartcity-rg \
  --plan smartcity-plan --name smartcity-app \
  --deployment-container-image-name smartcityregistry.azurecr.io/smartcity-api:latest

# 7. Configure app
az webapp config container set --name smartcity-app \
  --resource-group smartcity-rg \
  --docker-custom-image-name smartcityregistry.azurecr.io/smartcity-api:latest \
  --docker-registry-server-url https://smartcityregistry.azurecr.io \
  --docker-registry-server-user <username> \
  --docker-registry-server-password <password>
```

---

## Production Configuration

### Environment Variables

Create `.env.production`:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False
API_WORKERS=4

# Security
SECRET_KEY=your-very-secure-secret-key-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (if using database)
DATABASE_URL=postgresql://user:password@db-host:5432/smartcity
DATABASE_POOL_SIZE=20

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/smartcity/app.log

# Features
ENABLE_CACHING=True
CACHE_TTL=300
ENABLE_ANALYTICS=True

# Third-party services
WEATHER_API_KEY=your-api-key
TRAFFIC_API_KEY=your-api-key
```

### Nginx Configuration

Create `nginx.conf`:

```nginx
upstream api {
    server api:8000;
}

upstream dashboard {
    server dashboard:8501;
}

server {
    listen 80;
    server_name yourdomain.com;
    client_max_body_size 100M;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # API proxy
    location /api/ {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Dashboard proxy
    location / {
        proxy_pass http://dashboard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Streamlit specific settings
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

---

## Monitoring and Logging

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check with interval
watch -n 5 'curl -s http://localhost:8000/health | jq'
```

### Log Management

```bash
# View logs from all services
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f dashboard

# Save logs to file
docker-compose logs > logs.txt
```

### Performance Monitoring

```bash
# Check Docker resource usage
docker stats

# Monitor API performance
curl -X POST http://localhost:8000/api/v1/predict/traffic \
  -H "Content-Type: application/json" \
  -d '{"car_count": 100, "bike_count": 50, "bus_count": 10, "truck_count": 5}'
```

---

## Troubleshooting

### Common Issues

#### 1. Models not loaded
```bash
# Check if models exist
ls -la models/

# Train models
python train_models.py

# Check logs
docker-compose logs api | grep -i "model"
```

#### 2. Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
docker-compose up -e API_PORT=8001
```

#### 3. Permission denied
```bash
# Fix file permissions
chmod -R 755 models/
chmod -R 755 datasets/

# Fix Docker socket permission (if needed)
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. Memory issues
```bash
# Increase Docker memory limit
# Edit docker-compose.yml and add:
# services:
#   api:
#     deploy:
#       resources:
#         limits:
#           memory: 2G
```

#### 5. Database connection errors
```bash
# Check database connection
docker-compose exec api python -c "import psycopg2; psycopg2.connect('postgresql://...')"

# Check environment variables
docker-compose config | grep DATABASE_URL
```

### Getting Help

1. Check logs: `docker-compose logs -f`
2. Check health: `curl http://localhost:8000/health`
3. Review API docs: `http://localhost:8000/api/docs`
4. Create issue on GitHub with logs and configuration

---

## Performance Optimization

### Caching
```python
# In main.py, enable response caching
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend
```

### Async Processing
- Use background tasks for long-running operations
- Implement message queues (Redis, RabbitMQ)

### Load Balancing
- Use multiple API workers: `uvicorn ... --workers 4`
- Deploy behind load balancer (Nginx, HAProxy)

---

## Maintenance

### Regular Tasks

```bash
# Weekly: Check logs and clean up
docker-compose logs > backup_logs.txt
docker system prune -a --volumes

# Monthly: Update dependencies
pip list --outdated
pip install -r requirements.txt --upgrade

# Update models
python train_models.py

# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz models/ datasets/
```

---

For more information, see [README.md](../README.md) or visit the [official documentation](https://docs.smartcity-ml.com).
