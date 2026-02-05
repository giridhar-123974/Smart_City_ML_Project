from fastapi import FastAPI
import joblib

app = FastAPI(title="Smart City ML Platform")

# Load models
air_model = joblib.load("../models/air_quality_random_forest.pkl")
energy_model = joblib.load("../models/energy_random_forest.pkl")
traffic_model = joblib.load("../models/traffic_random_forest.pkl")

@app.get("/")
def home():
    return {"message": "Smart City ML API is running"}

@app.post("/air/predict")
def predict_air(data: list):
    prediction = air_model.predict([data])[0]
    return {"Predicted_CO": prediction}

@app.post("/energy/predict")
def predict_energy(data: list):
    prediction = energy_model.predict([data])[0]
    return {"Predicted_Energy": prediction}

@app.post("/traffic/predict")
def predict_traffic(data: list):
    prediction = traffic_model.predict([data])[0]
    return {"Traffic_Level": int(prediction)}
