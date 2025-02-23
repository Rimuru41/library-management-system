import os

class Config:
    # General Configuration
    SECRET_KEY = os.environ.get('LIBRARY_SECRET_KEY')  # Default for development
    SESSION_COOKIE_NAME = 'library_session'
    UPLOAD_FOLDER = os.path.join('app','static', 'images', 'books')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Database Configuration
    DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://library_management_system_wjn9_user:frSKvA4ATQFo8vMDzGvczAZDfPkCD9Tu@dpg-cut84m5umphs73cg9se0-a.oregon-postgres.render.com/library_management_system_wjn9')

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
    DATABASE_URI = 'postgresql://library_management_system_wjn9_user:frSKvA4ATQFo8vMDzGvczAZDfPkCD9Tu@dpg-cut84m5umphs73cg9se0-a.oregon-postgres.render.com/library_management_system_wjn9'


