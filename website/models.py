"""
Database models for Smart City application
"""

from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Prediction(db.Model):
    """Model to store prediction history"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    prediction_type = db.Column(db.String(50), nullable=False)  # traffic, air_quality, energy
    input_data = db.Column(db.JSON, nullable=False)
    prediction_result = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Prediction {self.prediction_type} - {self.prediction_result}>'


class PredictionHistory(db.Model):
    """Store statistics about predictions"""
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_type = db.Column(db.String(50), nullable=False, index=True)
    average_value = db.Column(db.Float, nullable=False)
    total_predictions = db.Column(db.Integer, default=1)
    date = db.Column(db.Date, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<PredictionHistory {self.prediction_type} - {self.date}>'
