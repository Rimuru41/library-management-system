from flask import Flask
from app.config import DevelopmentConfig,ProductionConfig # Import the config class
from .routes import main
from dotenv import load_dotenv
load_dotenv()

def create_app():

    app = Flask(__name__)


    app.config.from_object(DevelopmentConfig)
   #df 
    print("SECRET_KEY:", app.config.get('SECRET_KEY'))


    print(f"DEBUG mode: {app.config['DEBUG']}")  

    # Register Blueprints 

    app.register_blueprint(main)

    return app
