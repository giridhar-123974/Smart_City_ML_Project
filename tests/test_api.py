"""
Unit tests for Smart City ML API
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "models_loaded" in data
        assert "timestamp" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["version"] == "1.0.0"


class TestAirQualityPrediction:
    """Test air quality prediction endpoints"""
    
    def test_air_quality_valid_request(self):
        """Test valid air quality prediction"""
        payload = {
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
        }
        
        response = client.post("/api/v1/predict/air-quality", json=payload)
        assert response.status_code == 200 or response.status_code == 503
    
    def test_air_quality_missing_field(self):
        """Test air quality prediction with missing field"""
        payload = {
            "PT08_S1_CO": 1360.0,
            "NMHC_GT": 150.0,
            # Missing other required fields
        }
        
        response = client.post("/api/v1/predict/air-quality", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_air_quality_negative_value(self):
        """Test air quality prediction with negative values"""
        payload = {
            "PT08_S1_CO": -1360.0,  # Invalid negative value
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
        }
        
        response = client.post("/api/v1/predict/air-quality", json=payload)
        assert response.status_code == 422  # Validation error


class TestTrafficPrediction:
    """Test traffic prediction endpoints"""
    
    def test_traffic_valid_request(self):
        """Test valid traffic prediction"""
        payload = {
            "car_count": 100,
            "bike_count": 50,
            "bus_count": 10,
            "truck_count": 5
        }
        
        response = client.post("/api/v1/predict/traffic", json=payload)
        assert response.status_code == 200 or response.status_code == 503
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "traffic_level" in data
            assert "recommendations" in data
    
    def test_traffic_zero_vehicles(self):
        """Test traffic prediction with zero vehicles"""
        payload = {
            "car_count": 0,
            "bike_count": 0,
            "bus_count": 0,
            "truck_count": 0
        }
        
        response = client.post("/api/v1/predict/traffic", json=payload)
        assert response.status_code == 200 or response.status_code == 503
    
    def test_traffic_large_numbers(self):
        """Test traffic prediction with large vehicle counts"""
        payload = {
            "car_count": 10000,
            "bike_count": 5000,
            "bus_count": 1000,
            "truck_count": 500
        }
        
        response = client.post("/api/v1/predict/traffic", json=payload)
        assert response.status_code == 200 or response.status_code == 503


class TestEnergyPrediction:
    """Test energy prediction endpoints"""
    
    def test_energy_valid_request(self):
        """Test valid energy prediction"""
        payload = {
            "features": [1.5, 2.3, 3.1, 2.8]
        }
        
        response = client.post("/api/v1/predict/energy", json=payload)
        assert response.status_code == 200 or response.status_code == 503
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "unit" in data
    
    def test_energy_empty_features(self):
        """Test energy prediction with empty features"""
        payload = {
            "features": []
        }
        
        response = client.post("/api/v1/predict/energy", json=payload)
        assert response.status_code == 422 or response.status_code == 503
    
    def test_energy_single_feature(self):
        """Test energy prediction with single feature"""
        payload = {
            "features": [2.5]
        }
        
        response = client.post("/api/v1/predict/energy", json=payload)
        assert response.status_code == 200 or response.status_code == 503


class TestBatchPredictions:
    """Test batch prediction endpoints"""
    
    def test_batch_air_quality_valid(self):
        """Test valid batch air quality predictions"""
        payload = [
            {
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
            }
        ]
        
        response = client.post("/api/v1/predict/batch/air-quality", json=payload)
        assert response.status_code == 200 or response.status_code == 503
        
        if response.status_code == 200:
            data = response.json()
            assert "predictions" in data
            assert "count" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
