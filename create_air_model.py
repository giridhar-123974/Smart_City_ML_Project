import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Create a simple air quality model
X_dummy = np.random.rand(100, 10)
y_dummy = np.random.rand(100) * 500

model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_dummy, y_dummy)

joblib.dump(model, 'models/air_quality_model.pkl')
print('✓ Air quality model created')
