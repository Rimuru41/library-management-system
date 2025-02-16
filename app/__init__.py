from flask import Flask
from app.config import DevelopmentConfig,ProductionConfig # Import the config class
from .routes import main
def create_app():

    app = Flask(__name__)


    app.config.from_object(DevelopmentConfig)
   #df 
    print(f"SECRET_KEY: {app.config['SECRET_KEY']}")  # Check if SECRET_KEY is being loaded correctly


    print(f"DEBUG mode: {app.config['DEBUG']}")  

    # Register Blueprints 

    app.register_blueprint(main)

    return app
