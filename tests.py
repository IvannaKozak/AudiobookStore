import pytest
from main import app, db
from models import Category, Audiobook

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


def test_get_categories(client):
    # Adding a category for testing the GET endpoint
    client.post('/category/', json={'category_name': 'Science'})

    response = client.get('/category/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['category_name'] == 'Science'


def test_delete_category(client):
    # Adding a category to delete
    post_response = client.post('/category/', json={'category_name': 'Fiction'})
    category_id = post_response.get_json()['id']

    # Deleting the added category
    delete_response = client.delete(f'/category/{category_id}')
    assert delete_response.status_code == 200

    # Verify if category is deleted by trying to fetch it
    get_response = client.get('/category/')
    data = get_response.get_json()
    category = next((cat for cat in data if cat['id'] == category_id), None)
    assert category is None


def test_update_category(client):
    # Adding a category to update
    post_response = client.post('/category/', json={'category_name': 'Biography'})
    category_id = post_response.get_json()['id']

    # Updating the added category
    update_response = client.put(f'/category/{category_id}', json={'category_name': 'Detective'})
    assert update_response.status_code == 200

    # Verify if category is updated
    get_response = client.get('/category/')
    data = get_response.get_json()
    updated_category = next((category for category in data if category['id'] == category_id), None)
    assert updated_category is not None
    assert updated_category['category_name'] == 'Detective'



# Utility function to add an audiobook for testing
def add_test_audiobook(client, title="Test Audiobook", description="A test description", category_id=None):
    return client.post('/audiobook/', json={
        'title': title, 
        'description': description,
        'category_id': category_id
    })

# Test the GET endpoint
def test_get_audiobooks(client):
    response = client.get('/audiobook/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Check if data is a list

# Test the POST endpoint
def test_add_audiobook(client):
    response = add_test_audiobook(client)
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data

# Test the DELETE endpoint
def test_delete_audiobook(client):
    # First add an audiobook to delete
    add_response = add_test_audiobook(client)
    audiobook_id = add_response.get_json()['id']

    # Now delete the audiobook
    del_response = client.delete(f'/audiobook/{audiobook_id}')
    assert del_response.status_code == 200

# Test the PUT endpoint
def test_update_audiobook(client):
    # First add an audiobook to update
    add_response = add_test_audiobook(client)
    audiobook_id = add_response.get_json()['id']

    # Now update the audiobook
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated Description',
    }
    update_response = client.put(f'/audiobook/{audiobook_id}', json=update_data)
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data['message'] == "Audiobook updated"