from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from .routes import main
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import check_and_apply_fines, check_and_apply_reservations, update_book_copies

load_dotenv()

def create_app(config_object=None):
    app = Flask(__name__)

    # Load configuration based on a parameter or default to ProductionConfig
    if config_object:
        print("IN Testing")
        app.config.from_object(config_object)
    else:
        app.config.from_object(ProductionConfig)

    print("SECRET_KEY:", app.config.get('SECRET_KEY'))
    print(f"DEBUG mode: {app.config['DEBUG']}")  
    print(f'Database URI: {app.config["DATABASE_URI"]}')

    # Register BlueprintsTestingConfig
    app.register_blueprint(main)

    # Function to check and update fines
    def check_fines_background():
        overdue_books = check_and_apply_fines()
        if overdue_books:
            for copy_id in overdue_books:
                update_book_copies(copy_id, 'Available')

    # Function to expire reservations
    def expire_reservations_background():
        expired_reserve = check_and_apply_reservations()
        if expired_reserve:
            for copy_id in expired_reserve:
                update_book_copies(copy_id, 'Available')

    # Initialize APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_fines_background, 'interval', hours=1)
    scheduler.add_job(expire_reservations_background, 'interval', hours=1)
    scheduler.start()

    return app
