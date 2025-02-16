import os

class Config:
    # General Configuration
    SECRET_KEY = os.environ.get('LIBRARY_SECRET_KEY')  # Default for development
    SESSION_COOKIE_NAME = 'library_session'

    # Database Configuration
    DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://username:password@localhost/library_management_system')

    # Debug and Testing (Explicit boolean handling)
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    TESTING = os.environ.get('FLASK_TESTING', 'False').lower() in ['true', '1', 'yes']

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Ensure cookies are transmitted over HTTPS

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URI = 'postgresql://postgres@localhost/library_management_system'  # Use a separate test DB
