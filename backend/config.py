import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///concierge.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    API_KEY = os.environ.get('API_KEY', 'default-api-key-change-in-production')
    
    # CORS configuration - comma-separated list of allowed origins
    # Example: "http://localhost:3000,https://app.example.com"
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
