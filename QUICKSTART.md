# Quick Reference Guide

## 🚀 Get Started in 2 Minutes

### Windows Users
```bash
setup.bat
```

### Mac/Linux Users
```bash
chmod +x setup.sh
./setup.sh
```

### Using Docker (Recommended)
```bash
docker-compose up --build
```

---

## 📍 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| API Docs | http://localhost:8000/api/docs | Interactive API documentation |
| API ReDoc | http://localhost:8000/api/redoc | Alternative API documentation |
| Dashboard | http://localhost:8501 | Interactive dashboard |
| Health Check | http://localhost:8000/health | System status |

---

## 🔧 Common Commands

### Training Models
```bash
cd Smart_City_ML_Project
python train_models.py
```

### Running API Server
```bash
cd Smart_City_ML_Project
python -m uvicorn backend.main:app --reload
```

### Running Dashboard
```bash
cd Smart_City_ML_Project
streamlit run dashboard/app.py
```

### Docker Commands
```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f api
docker-compose logs -f dashboard

# Stop services
docker-compose down

# Clean up everything
docker-compose down -v
```

### Testing
```bash
pytest tests/ -v
pytest tests/test_api.py::TestHealthCheck -v
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `train_models.py` | Train ML models |
| `backend/main.py` | FastAPI backend |
| `dashboard/app.py` | Streamlit dashboard |
| `docker-compose.yml` | Container orchestration |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables |
| `README.md` | Project documentation |
| `DEPLOYMENT.md` | Deployment guide |
| `COMPLETION.md` | Detailed completion summary |

---

## 🌐 API Endpoints

### Health & Status
```
GET /health                          Health check
GET /                                API info
```

### Air Quality Predictions
```
POST /api/v1/predict/air-quality     Single prediction
POST /api/v1/predict/batch/air-quality  Batch predictions
```

### Traffic Predictions
```
POST /api/v1/predict/traffic         Traffic prediction
```

### Energy Predictions
```
POST /api/v1/predict/energy          Energy prediction
```

---

## 🐳 Docker Quick Tips

### View Service Logs
```bash
docker-compose logs -f api          # API logs
docker-compose logs -f dashboard    # Dashboard logs
docker-compose logs                 # All logs
```

### Access Container Shell
```bash
docker-compose exec api sh
docker-compose exec dashboard sh
```

### Restart Services
```bash
docker-compose restart api
docker-compose restart dashboard
docker-compose restart
```

### Check Resource Usage
```bash
docker stats
```

---

## 🚨 Troubleshooting

### Models Not Loading
```bash
python train_models.py
docker-compose restart api
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
kill -9 <PID>

# Or use different port
docker-compose up -e API_PORT=8001
```

### Permission Denied
```bash
chmod -R 755 models/
chmod -R 755 datasets/
```

### Docker Issues
```bash
docker system prune -a
docker-compose down -v
docker-compose up --build
```

---

## 📊 Dashboard Pages

1. **Dashboard Overview** - System status, key metrics
2. **Traffic Control** - Traffic prediction and recommendations
3. **Air Quality Monitor** - Pollution level predictions
4. **Energy Intelligence** - Energy consumption forecasting
5. **Analytics & Reports** - Performance metrics and visualizations

---

## 🔐 Environment Configuration

Key variables in `.env`:
- `API_HOST` - API host address
- `API_PORT` - API port (default: 8000)
- `API_DEBUG` - Debug mode (False for production)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, etc.)

---

## 📝 Example API Calls

### Air Quality Prediction
```bash
curl -X POST http://localhost:8000/api/v1/predict/air-quality \
  -H "Content-Type: application/json" \
  -d '{
    "PT08_S1_CO": 1360.0,
    "NMHC_GT": 150.0,
    "C6H6_GT": 11.9,
    "PT08_S2_NMHC": 1046.0,
    "NOx_GT": 166.0,
    "PT08_S3_NOx": 1056.0,
    "NO2_GT": 113.0,
    "PT08_S4_NO2": 1692.0,
    "PT08_S5_O3": 1268.0,
    "temperature": 13.6,
    "humidity": 48.9,
    "absolute_humidity": 0.7578
  }'
```

### Traffic Prediction
```bash
curl -X POST http://localhost:8000/api/v1/predict/traffic \
  -H "Content-Type: application/json" \
  -d '{
    "car_count": 100,
    "bike_count": 50,
    "bus_count": 10,
    "truck_count": 5
  }'
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## 🚀 Deployment Checklist

- [ ] Run `python train_models.py`
- [ ] Test with `docker-compose up`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Push to GitHub
- [ ] Configure deployment platform (Heroku/AWS/Azure)
- [ ] Set environment variables
- [ ] Deploy
- [ ] Test endpoints
- [ ] Monitor logs

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Completion Summary**: See `COMPLETION.md`
- **API Documentation**: http://localhost:8000/api/docs
- **GitHub Actions**: `.github/workflows/`

---

## ⚡ Performance Tips

- Models are cached in Streamlit for faster dashboard loads
- Use Docker for consistent environments
- Enable Gzip compression in nginx for faster transfers
- Scale API with multiple workers: `uvicorn ... --workers 4`
- Use caching middleware for frequently accessed endpoints

---

## 🎯 Next Steps

1. **Today**: Run `docker-compose up --build` and test
2. **Week 1**: Push to GitHub and configure CI/CD
3. **Week 2**: Deploy to production cloud platform
4. **Month 1**: Integrate real data sources and monitor

---

## 📞 Support

For issues:
1. Check DEPLOYMENT.md troubleshooting section
2. Review Docker logs: `docker-compose logs -f`
3. Check health endpoint: `curl http://localhost:8000/health`
4. Review API documentation: http://localhost:8000/api/docs

---

**Ready to deploy? Type: `docker-compose up --build`** 🚀
