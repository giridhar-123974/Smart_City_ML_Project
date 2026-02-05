"""
Application routes - Main, Auth, and API endpoints
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Prediction
from .ml_models import get_model_manager
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get user statistics
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    
    # Get recent predictions
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.created_at.desc()).limit(5).all()
    
    # Get prediction breakdown
    traffic_count = Prediction.query.filter_by(user_id=current_user.id, 
                                              prediction_type='traffic').count()
    air_count = Prediction.query.filter_by(user_id=current_user.id, 
                                          prediction_type='air_quality').count()
    energy_count = Prediction.query.filter_by(user_id=current_user.id, 
                                             prediction_type='energy').count()
    
    return render_template('dashboard.html',
                         total_predictions=total_predictions,
                         recent_predictions=recent_predictions,
                         traffic_count=traffic_count,
                         air_count=air_count,
                         energy_count=energy_count)

@main_bp.route('/traffic')
@login_required
def traffic():
    """Traffic prediction page"""
    return render_template('traffic.html')

@main_bp.route('/air-quality')
@login_required
def air_quality():
    """Air quality prediction page"""
    return render_template('air_quality.html')

@main_bp.route('/energy')
@login_required
def energy():
    """Energy prediction page"""
    return render_template('energy.html')

@main_bp.route('/history')
@login_required
def history():
    """Prediction history page"""
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.created_at.desc()).all()
    return render_template('history.html', predictions=predictions)

# ==================== AUTHENTICATION ROUTES ====================

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            return render_template('signup.html', error='All fields required'), 400
        
        if password != password_confirm:
            return render_template('signup.html', error='Passwords do not match'), 400
        
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters'), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error='Username already exists'), 400
        
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error='Email already registered'), 400
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'New user registered: {username}')
        return redirect(url_for('auth.login', message='Signup successful! Please log in.'))
    
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not all([username, password]):
            return render_template('login.html', error='Username and password required'), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            logger.info(f'User logged in: {username}')
            return redirect(url_for('main.dashboard'))
        
        return render_template('login.html', error='Invalid username or password'), 401
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logger.info(f'User logged out: {current_user.username}')
    logout_user()
    return redirect(url_for('main.index'))

# ==================== API ROUTES ====================

@api_bp.route('/predict/traffic', methods=['POST'])
@login_required
def predict_traffic():
    """Traffic prediction API"""
    try:
        data = request.get_json()
        model_manager = get_model_manager()
        
        if not model_manager:
            return jsonify({'error': 'Model manager not initialized'}), 500
        
        # Validate input
        required_fields = ['hour', 'day_of_week', 'vehicle_count', 'avg_speed', 'weather']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Make prediction
        result = model_manager.predict_traffic(data)
        
        if result.get('status') == 'error':
            return jsonify(result), 400
        
        # Store prediction in database
        prediction = Prediction(
            user_id=current_user.id,
            prediction_type='traffic',
            input_data=data,
            prediction_result=result['prediction'],
            confidence=result['confidence']
        )
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f'Error in traffic prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/predict/air-quality', methods=['POST'])
@login_required
def predict_air_quality():
    """Air quality prediction API"""
    try:
        data = request.get_json()
        model_manager = get_model_manager()
        
        if not model_manager:
            return jsonify({'error': 'Model manager not initialized'}), 500
        
        # Make prediction
        result = model_manager.predict_air_quality(data)
        
        if result.get('status') == 'error':
            return jsonify(result), 400
        
        # Store prediction in database
        prediction = Prediction(
            user_id=current_user.id,
            prediction_type='air_quality',
            input_data=data,
            prediction_result=result['aqi']
        )
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f'Error in air quality prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/predict/energy', methods=['POST'])
@login_required
def predict_energy():
    """Energy prediction API"""
    try:
        data = request.get_json()
        model_manager = get_model_manager()
        
        if not model_manager:
            return jsonify({'error': 'Model manager not initialized'}), 500
        
        # Make prediction
        result = model_manager.predict_energy(data)
        
        if result.get('status') == 'error':
            return jsonify(result), 400
        
        # Store prediction in database
        prediction = Prediction(
            user_id=current_user.id,
            prediction_type='energy',
            input_data=data,
            prediction_result=result['consumption_kwh']
        )
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f'Error in energy prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/history/<prediction_type>')
@login_required
def get_history(prediction_type):
    """Get prediction history for a type"""
    predictions = Prediction.query.filter_by(
        user_id=current_user.id,
        prediction_type=prediction_type
    ).order_by(Prediction.created_at.desc()).all()
    
    return jsonify({
        'data': [{
            'id': p.id,
            'result': p.prediction_result,
            'confidence': p.confidence,
            'created_at': p.created_at.isoformat()
        } for p in predictions]
    })

@api_bp.route('/stats/dashboard')
@login_required
def stats_dashboard():
    """Get dashboard statistics"""
    total = Prediction.query.filter_by(user_id=current_user.id).count()
    traffic = Prediction.query.filter_by(user_id=current_user.id, 
                                        prediction_type='traffic').count()
    air = Prediction.query.filter_by(user_id=current_user.id, 
                                    prediction_type='air_quality').count()
    energy = Prediction.query.filter_by(user_id=current_user.id, 
                                       prediction_type='energy').count()
    
    return jsonify({
        'total': total,
        'traffic': traffic,
        'air_quality': air,
        'energy': energy
    })
