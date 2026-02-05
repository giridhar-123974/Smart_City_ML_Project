"""
ML Model Management - Load and use trained models
"""

import joblib
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages loading and using ML models"""
    
    def __init__(self, models_dir='./models'):
        self.models_dir = models_dir
        self.models = {}
        self.load_all_models()
    
    def load_all_models(self):
        """Load all trained models"""
        try:
            # Load traffic model
            traffic_model_path = os.path.join(self.models_dir, 'traffic_model.pkl')
            if os.path.exists(traffic_model_path):
                self.models['traffic'] = joblib.load(traffic_model_path)
                logger.info("✓ Traffic model loaded")
            else:
                logger.warning(f"Traffic model not found at {traffic_model_path}")
                self.models['traffic'] = None
            
            # Load air quality model
            air_model_path = os.path.join(self.models_dir, 'air_quality_model.pkl')
            if os.path.exists(air_model_path):
                self.models['air_quality'] = joblib.load(air_model_path)
                logger.info("✓ Air quality model loaded")
            else:
                logger.warning(f"Air quality model not found at {air_model_path}")
                self.models['air_quality'] = None
            
            # Load energy model
            energy_model_path = os.path.join(self.models_dir, 'energy_model.pkl')
            if os.path.exists(energy_model_path):
                self.models['energy'] = joblib.load(energy_model_path)
                logger.info("✓ Energy model loaded")
            else:
                logger.warning(f"Energy model not found at {energy_model_path}")
                self.models['energy'] = None
        
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
    def predict_traffic(self, features_dict):
        """
        Predict traffic congestion
        
        Features required:
        - hour: 0-23
        - day_of_week: 0-6
        - vehicle_count: int
        - avg_speed: float
        - weather: 0=sunny, 1=rainy, 2=foggy
        """
        try:
            if self.models['traffic'] is None:
                return {'error': 'Traffic model not loaded', 'status': 'error'}
            
            # Prepare features
            features = np.array([[
                features_dict.get('hour', 0),
                features_dict.get('day_of_week', 0),
                features_dict.get('vehicle_count', 0),
                features_dict.get('avg_speed', 0),
                features_dict.get('weather', 0)
            ]])
            
            prediction = self.models['traffic'].predict(features)[0]
            probability = self.models['traffic'].predict_proba(features)[0]
            
            labels = ['Low', 'Medium', 'High']
            
            return {
                'prediction': int(prediction),
                'label': labels[int(prediction)],
                'confidence': float(max(probability)),
                'status': 'success'
            }
        
        except Exception as e:
            logger.error(f"Error in traffic prediction: {str(e)}")
            return {'error': str(e), 'status': 'error'}
    
    def predict_air_quality(self, features_dict):
        """
        Predict air quality index
        
        Features: various sensor readings
        """
        try:
            if self.models['air_quality'] is None:
                return {'error': 'Air quality model not loaded', 'status': 'error'}
            
            features = np.array([[features_dict.get(f'feature_{i}', 0) for i in range(10)]])
            prediction = self.models['air_quality'].predict(features)[0]
            
            return {
                'aqi': float(prediction),
                'status': 'success'
            }
        
        except Exception as e:
            logger.error(f"Error in air quality prediction: {str(e)}")
            return {'error': str(e), 'status': 'error'}
    
    def predict_energy(self, features_dict):
        """
        Predict energy consumption
        
        Features: various consumption-related inputs
        """
        try:
            if self.models['energy'] is None:
                return {'error': 'Energy model not loaded', 'status': 'error'}
            
            features = np.array([[features_dict.get(f'feature_{i}', 0) for i in range(5)]])
            prediction = self.models['energy'].predict(features)[0]
            
            return {
                'consumption_kwh': float(prediction),
                'status': 'success'
            }
        
        except Exception as e:
            logger.error(f"Error in energy prediction: {str(e)}")
            return {'error': str(e), 'status': 'error'}

# Create global model manager instance
model_manager = None

def init_model_manager(models_dir):
    """Initialize model manager"""
    global model_manager
    model_manager = ModelManager(models_dir)
    return model_manager

def get_model_manager():
    """Get model manager instance"""
    return model_manager
