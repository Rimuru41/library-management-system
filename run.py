# run.py
from app import create_app  
from app.config import DevelopmentConfig, ProductionConfig,TestingConfig
import os

app = create_app(ProductionConfig)  
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 for local, but Render provides a PORT env
    app.run(host="0.0.0.0", port=port)