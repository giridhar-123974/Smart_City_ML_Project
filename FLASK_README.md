# 🏙️ Smart City ML Flask Application

A professional-grade full-stack web application for Smart City predictions with Machine Learning models for Traffic, Air Quality, and Energy Management.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Using the Application](#using-the-application)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Development](#development)

---

## ✨ Features

### 🚦 Traffic Prediction
- Predicts traffic congestion levels (Low/Medium/High)
- Input: Hour, Day of Week, Vehicle Count, Average Speed, Weather
- Model: Random Forest Classifier (85%+ accuracy)

### 💨 Air Quality Index
- Predicts air quality index (AQI) based on sensor readings
- 10 sensor inputs for comprehensive analysis
- Model: Random Forest Regressor

### ⚡ Energy Consumption
- Predicts energy consumption in kWh
- Factors: Temperature, Humidity, Time, Building Load, Usage Factor
- Model: Random Forest Regressor

### 👤 User Management
- Signup/Login authentication
- Secure password hashing
- User-specific prediction history

### 📊 Dashboard
- Real-time statistics
- Prediction history tracking
- Visual charts and insights

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Python Flask 3.0
- **Database**: SQLite (SQLAlchemy ORM)
- **Auth**: Flask-Login + Werkzeug password hashing
- **ML**: Scikit-learn, NumPy, Pandas
- **Server**: Gunicorn (production)

### Frontend
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome 6
- **API**: Fetch API (async/await)
- **Template Engine**: Jinja2

### Development
- **Testing**: Pytest
- **Environment**: Python 3.8+
- **Package Manager**: pip

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Option 1: Windows Batch Script (Easiest)

```bash
# Simply run:
RUN_FLASK.bat
```

This will:
1. Create virtual environment
2. Install dependencies
3. Create necessary directories
4. Start the Flask server

### Option 2: Manual Setup

#### 1. Clone and navigate to project
```bash
cd Smart_City_ML_Project
```

#### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Create directories
```bash
mkdir models logs uploads
```

#### 5. Start application
```bash
python app.py
```

#### 6. Open in browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
Smart_City_ML_Project/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── setup.bat / setup.sh            # Setup scripts
├── RUN_FLASK.bat                   # Quick start (Windows)
│
├── website/
│   ├── __init__.py                 # Flask app factory
│   ├── models.py                   # Database models (User, Prediction)
│   ├── routes.py                   # Application routes
│   ├── ml_models.py                # ML model management
│   │
│   ├── templates/                  # HTML templates (Jinja2)
│   │   ├── base.html               # Base template with navigation
│   │   ├── index.html              # Landing page
│   │   ├── login.html              # Login page
│   │   ├── signup.html             # Signup page
│   │   ├── dashboard.html          # Main dashboard
│   │   ├── traffic.html            # Traffic prediction form
│   │   ├── air_quality.html        # Air quality prediction form
│   │   ├── energy.html             # Energy prediction form
│   │   └── history.html            # Prediction history
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Custom styles
│   │   └── js/
│   │       └── main.js             # JavaScript utilities
│
├── models/                         # Saved ML models (pickle files)
│   ├── traffic_model.pkl
│   ├── air_quality_model.pkl
│   └── energy_model.pkl
│
├── notebooks/                      # Jupyter notebooks for training
│   ├── 1_traffic_model.ipynb
│   ├── 2_air_quality_model.ipynb
│   └── 3_energy_model.ipynb
│
├── datasets/
│   ├── air_quality/
│   │   └── AirQuality.csv
│   ├── energy/
│   │   ├── KwhConsumptionBlower78_1.csv
│   │   ├── KwhConsumptionBlower78_2.csv
│   │   └── KwhConsumptionBlower78_3.csv
│   └── traffic/
│       ├── Traffic.csv
│       └── TrafficTwoMonth.csv
│
├── logs/                           # Application logs
└── uploads/                        # User uploads
```

---

## 📖 Using the Application

### 1. First Time Setup

**Sign Up**
- Click "Sign Up" on the landing page
- Enter username, email, and password (min 6 chars)
- Confirm password
- Click "Sign Up"

**Login**
- Click "Login"
- Enter your credentials
- Click "Login"

### 2. Making Predictions

#### Traffic Prediction
1. Go to **Traffic** page
2. Set parameters:
   - Hour (0-23)
   - Day of Week
   - Vehicle Count
   - Average Speed (km/h)
   - Weather (Sunny/Rainy/Foggy)
3. Click **Predict**
4. View result (Low/Medium/High congestion)

#### Air Quality Prediction
1. Go to **Air Quality** page
2. Enter 10 sensor readings (0-100 range)
3. Click **Predict**
4. View AQI score and health recommendations

#### Energy Prediction
1. Go to **Energy** page
2. Set parameters:
   - Temperature (°C)
   - Humidity (%)
   - Time of Day (0-23)
   - Building Load (kW)
   - Usage Factor (0-1)
3. Click **Predict**
4. View forecasted consumption in kWh

### 3. Dashboard

**Statistics**
- Total predictions made
- Count by type (Traffic/Air/Energy)

**Quick Actions**
- Fast links to prediction pages

**Recent Predictions**
- Last 5 predictions table
- Type, result, and timestamp

### 4. History

- View all predictions
- Filter by type (optional)
- Sort by date
- Download/export (in future updates)

---

## 🔌 API Endpoints

All API endpoints require authentication (login).

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | User registration |
| POST | `/auth/login` | User login |
| GET | `/auth/logout` | User logout |

### Pages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/dashboard` | Main dashboard |
| GET | `/traffic` | Traffic prediction page |
| GET | `/air-quality` | Air quality prediction page |
| GET | `/energy` | Energy prediction page |
| GET | `/history` | Prediction history page |

### Prediction API
| Method | Endpoint | Body | Returns |
|--------|----------|------|---------|
| POST | `/api/predict/traffic` | `{hour, day_of_week, vehicle_count, avg_speed, weather}` | `{prediction, label, confidence}` |
| POST | `/api/predict/air-quality` | `{feature_0...feature_9}` | `{aqi}` |
| POST | `/api/predict/energy` | `{feature_0...feature_4}` | `{consumption_kwh}` |

### History & Stats
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/history/<type>` | Get prediction history for type |
| GET | `/api/stats/dashboard` | Get dashboard statistics |

---

## 🚀 Deployment

### Local Deployment (Already Explained Above)

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add Procfile** (already in project)
   ```
   web: gunicorn app:app
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Railway.app Deployment

1. **Connect GitHub**
   - Go to railway.app
   - Connect your GitHub account
   - Select repository

2. **Set Environment**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   ```

3. **Deploy**
   - Railway auto-deploys on push

### Render Deployment

1. **Create Account**
   - Go to render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Select repository
   - Environment: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

3. **Deploy**
   - Click "Deploy"

---

## 👨‍💻 Development

### Training Models

Models are pre-trained and saved in `models/` folder. To retrain:

1. **Open Jupyter Notebook**
   ```bash
   jupyter notebook notebooks/1_traffic_model.ipynb
   ```

2. **Run cells** to retrain model

3. **Model is saved** automatically

### Adding Features

1. **Create new route** in `website/routes.py`
2. **Create template** in `website/templates/`
3. **Add styles** to `website/static/css/style.css`
4. **Add JavaScript** to `website/static/js/main.js`

### Database Migration

```bash
# Initialize migration
export FLASK_APP=app.py
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

### Testing

```bash
# Install pytest if not already
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=website
```

### Environment Variables (.env)

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///smartcity.db
MODELS_DIR=./models
```

---

## 📊 Model Information

### Traffic Model
- **Algorithm**: Random Forest Classifier
- **Features**: 5
- **Classes**: 3 (Low, Medium, High)
- **Accuracy**: 85%+
- **Training Samples**: 1000

### Air Quality Model
- **Algorithm**: Random Forest Regressor
- **Features**: 10 (sensor readings)
- **Target**: AQI (0-500+)
- **RMSE**: < 15

### Energy Model
- **Algorithm**: Random Forest Regressor
- **Features**: 5
- **Target**: kWh consumption
- **RMSE**: < 50 kWh

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(port=5001)
```

### Database Error
```bash
# Delete and recreate
rm smartcity.db
python app.py
```

### Models Not Loading
```bash
# Check models/ directory exists
# Train models using Jupyter notebooks
```

### Login Not Working
```bash
# Clear browser cookies
# Try in private/incognito mode
```

---

## 📝 License

Smart City ML Application - Open Source

## 👥 Support

For issues or questions:
1. Check this README
2. Review code comments
3. Check GitHub issues
4. Create new issue with details

---

## 🎯 Future Enhancements

- [ ] Real-time data integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] API documentation (Swagger)
- [ ] User permissions & roles
- [ ] Data export (CSV/PDF)
- [ ] Advanced ML models
- [ ] Real-time notifications

---

## 🌟 Credits

Built with Python, Flask, and Machine Learning

**Made with ❤️ for Smart Cities**
