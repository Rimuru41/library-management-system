import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.models.model_authentication import login_member,register_members
from app.models import get_db_connection
from flask.testing import FlaskClient
from app.config import TestingConfig 

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    # Explicitly set testing mode
    app.config['TESTING'] = True
    with app.test_client() as client:
         yield client

def test_config_loading():
    """Test that configuration settings load correctly."""
    app = create_app(TestingConfig)
    # Check that the testing config is active
    assert app.config['TESTING'] is True
    assert app.config['DEBUG'] is True

def test_home_route(client: FlaskClient):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_register_member():
    """Test registering a new member in the database."""
    result = register_members(
        "Test User", "test@example.com", "1234567890", 
        "Test Address", "2025-02-23", "hashed_password"
    )
    assert result in ['success', 'already_registered']

def test_login_member():
    """Test login function with a mock user."""
    result = login_member("test@example.com", "wrong_password")
    assert result == 'Not Registered' or (isinstance(result, (list, tuple)) and result[0] in ['success', 'staff', 'Twin'])

def test_database_connection():
    """Test database connection."""
    conn = get_db_connection()
    assert conn is not None
    conn.close()
