from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    cors_origins = app.config.get('CORS_ORIGINS', '*')
    if cors_origins != '*':
        cors_origins = [origin.strip() for origin in cors_origins.split(',')]
    CORS(app, resources={r"/api/*": {"origins": cors_origins, "supports_credentials": True}})
    db.init_app(app)
    JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.concerts import concerts_bp
    from routes.events import events_bp
    from routes.news import news_bp
    from routes.career import career_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(concerts_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(career_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'service': 'OpenClaw Concierge API'}
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
