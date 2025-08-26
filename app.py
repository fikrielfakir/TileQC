import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "ceramic-qc-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///instance/ceramic_qc.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Ensure SQLite uses UTF-8 encoding
if database_url.startswith('sqlite:'):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"]["connect_args"] = {
        "check_same_thread": False
    }

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # type: ignore

# Add custom Jinja2 filters
@app.template_filter('strftime')
def strftime_filter(date_str, fmt='%Y-%m-%d %H:%M:%S'):
    """Format datetime string or 'now' for current datetime"""
    if date_str == 'now':
        return datetime.now().strftime(fmt)
    elif isinstance(date_str, datetime):
        return date_str.strftime(fmt)
    else:
        try:
            # Try to parse string as datetime
            dt = datetime.fromisoformat(str(date_str))
            return dt.strftime(fmt)
        except:
            return str(date_str)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models
    import models
    
    # Create all tables
    db.create_all()
    
    # Initialize automation service
    from services.automation_service import automation_service
    automation_service.init_app(app)
    
    # Create default admin user if not exists
    from models import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@ceramic-qc.com'
        admin.password_hash = generate_password_hash('admin123')
        admin.role = 'admin'
        admin.full_name = 'System Administrator'
        db.session.add(admin)
        db.session.commit()
    
    # Initialize default specifications if none exist
    from models import Specification
    from utils.spec_defaults import initialize_default_specifications
    
    if Specification.query.count() == 0:
        total_created = 0
        control_types = ['clay', 'press', 'dryer', 'biscuit_kiln', 'email_kiln', 'dimensional', 'enamel']
        
        for control_type in control_types:
            created = initialize_default_specifications(control_type)
            total_created += created
        
        print(f"Initialized {total_created} default specifications")

# Register blueprints
from routes.main import main_bp
from routes.auth import auth_bp
from routes.clay import clay_bp
from routes.press import press_bp
from routes.dryer import dryer_bp
from routes.kilns import kilns_bp
from routes.enamel import enamel_bp
from routes.tests import tests_bp
from routes.reports import reports_bp
from routes.specifications import spec_bp
# from routes.optimized_measurements import optimized_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(clay_bp, url_prefix='/clay')
app.register_blueprint(press_bp, url_prefix='/press')
app.register_blueprint(dryer_bp, url_prefix='/dryer')
app.register_blueprint(kilns_bp, url_prefix='/kilns')
app.register_blueprint(enamel_bp, url_prefix='/enamel')
app.register_blueprint(tests_bp, url_prefix='/tests')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(spec_bp, url_prefix='/specifications')
# app.register_blueprint(optimized_bp, url_prefix='/optimized')
