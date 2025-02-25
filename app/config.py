import os

# Database connection details
DB_CONFIG = {
    'dbname': 'library_management_system_wjn9',
    'user': 'library_management_system_wjn9_user',
    'password': 'frSKvA4ATQFo8vMDzGvczAZDfPkCD9Tu',
    'host': 'dpg-cut84m5umphs73cg9se0-a.oregon-postgres.render.com',
    'port': '5432'
}

class Config:
    # General Configuration
    SECRET_KEY = os.environ.get('LIBRARY_SECRET_KEY')  # Default for development
    SESSION_COOKIE_NAME = 'library_session'
    UPLOAD_FOLDER = os.path.join('app','static', 'images', 'books')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
