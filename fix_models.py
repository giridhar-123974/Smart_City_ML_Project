#!/usr/bin/env python
"""
ML Model Training Script - Creates models with correct feature counts
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
import os

# Create models directory
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)

print("=" * 70)
print("TRAINING ML MODELS WITH CORRECT FEATURE COUNTS")
print("=" * 70)

# ============================================================================
# 1. TRAFFIC CONGESTION MODEL (5 features)
# ============================================================================
print("\n[1/3] Training Traffic Model (5 features)...")

np.random.seed(42)
n_samples = 1000

# Traffic: hour, day_of_week, vehicle_count, avg_speed, weather
X_traffic = np.random.rand(n_samples, 5)
X_traffic[:, 0] = np.random.randint(0, 24, n_samples)      # hour
X_traffic[:, 1] = np.random.randint(0, 7, n_samples)       # day_of_week
X_traffic[:, 2] = np.random.randint(10, 500, n_samples)    # vehicle_count
X_traffic[:, 3] = np.random.uniform(10, 80, n_samples)     # avg_speed
X_traffic[:, 4] = np.random.choice([0, 1, 2], n_samples)   # weather

# Create target based on rules
y_traffic = ((X_traffic[:, 2] > 250) * 2 + (X_traffic[:, 2] > 150) + 
             (X_traffic[:, 3] < 30)).astype(int).clip(0, 2)

traffic_model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
traffic_model.fit(X_traffic, y_traffic)

joblib.dump(traffic_model, os.path.join(models_dir, 'traffic_model.pkl'))
print(f"✓ Traffic model: {traffic_model.score(X_traffic, y_traffic):.2%} accuracy")
print(f"  Features: hour, day_of_week, vehicle_count, avg_speed, weather")

# ============================================================================
# 2. AIR QUALITY MODEL (10 features)
# ============================================================================
print("\n[2/3] Training Air Quality Model (10 features)...")

n_samples = 500

# Air quality: 10 sensor readings
X_air = np.random.rand(n_samples, 10)
for i in range(10):
    X_air[:, i] = np.random.uniform(0, 100, n_samples)

# Create AQI target
y_air = X_air.mean(axis=1) * 5 + np.random.normal(0, 5, n_samples)

air_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
air_model.fit(X_air, y_air)

joblib.dump(air_model, os.path.join(models_dir, 'air_quality_model.pkl'))
print(f"✓ Air quality model: R² = {air_model.score(X_air, y_air):.2%}")
print(f"  Features: 10 sensor readings")

# ============================================================================
# 3. ENERGY CONSUMPTION MODEL (5 features)
# ============================================================================
print("\n[3/3] Training Energy Model (5 features)...")

n_samples = 500

# Energy: temperature, humidity, hour, load, usage_factor
X_energy = np.random.rand(n_samples, 5)
X_energy[:, 0] = np.random.uniform(10, 35, n_samples)      # temperature
X_energy[:, 1] = np.random.uniform(30, 90, n_samples)      # humidity
X_energy[:, 2] = np.random.randint(0, 24, n_samples)       # hour
X_energy[:, 3] = np.random.uniform(50, 200, n_samples)     # building load
X_energy[:, 4] = np.random.uniform(0, 1, n_samples)        # usage factor

# Create consumption target
y_energy = (X_energy[:, 0] * 0.5 + X_energy[:, 3] * 0.3 + 
            X_energy[:, 4] * 50 + np.random.normal(0, 5, n_samples)).clip(0, 300)

energy_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
energy_model.fit(X_energy, y_energy)

joblib.dump(energy_model, os.path.join(models_dir, 'energy_model.pkl'))
print(f"✓ Energy model: R² = {energy_model.score(X_energy, y_energy):.2%}")
print(f"  Features: temperature, humidity, hour, load, usage_factor")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("✅ ALL MODELS TRAINED WITH CORRECT FEATURES")
print("=" * 70)
print("\nModel Feature Configuration:")
print("  • Traffic (Classifier): 5 features")
print("  • Air Quality (Regressor): 10 features")
print("  • Energy (Regressor): 5 features")
print("\nModels saved to: ./models/")
print("=" * 70)
