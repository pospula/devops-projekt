import pytest
from src.app import create_app
from src.models import db

@pytest.fixture
def client():
    # konfiguracja aplikacji pod testy (używam SQLite w pamięci dla izolacji)
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_health_check(client):
    """1. Test endpointu /health"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_create_user(client):
    """2. Test dodawania użytkownika"""
    response = client.post('/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'

def test_get_users(client):
    """3. Test pobierania listy użytkowników"""
    client.post('/users', json={'username': 'user1', 'email': 'user1@example.com'})
    
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['username'] == 'user1'