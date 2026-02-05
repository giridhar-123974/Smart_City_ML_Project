"""
Smart City ML Flask Application Entry Point
Run with: python app.py
"""

import os
from website import create_app, db
from website.models import User, Prediction

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell"""
    return {
        'db': db,
        'User': User,
        'Prediction': Prediction
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('✓ Database initialized')

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
