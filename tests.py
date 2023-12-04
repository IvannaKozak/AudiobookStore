import pytest
from main import app, db
from models import Category

# pytest tests.py  - to run the tests

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            token = generate_token()
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        yield client
        with app.app_context():
            db.drop_all()



import jwt
from datetime import datetime, timedelta

def generate_token():
    SECRET_KEY = "1bc991a9acbaf16a0183effe123615d85e3d7b1c17d1541pf8e869df41654a39"
    ALGORITHM = "HS256"

    # Example user details - you might want to adjust these for testing
    user_details = {
        'username': 'testuser',
        'id': 1,  # Example user ID
        'role': 'testrole'
    }

    # Token expiration time
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    # Encode and return token
    token_payload = {
        'sub': user_details['username'],
        'id': user_details['id'],
        'role': user_details['role'],
        'exp': expiration_time
    }

    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return token



def test_add_category(client):
    # Example test
    response = client.post('/category/', json={'category_name': 'History'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data