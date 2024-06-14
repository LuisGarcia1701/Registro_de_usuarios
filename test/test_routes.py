import pytest
from app import app, db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.drop_all()

def test_register(client):
    response = client.post('/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'password': 'Password123!',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'CA',
        'zip_code': '12345',
        'country': 'USA',
        'area': 'IT',
        'group': 'Development',
        'department': 'Software'
    }, follow_redirects=True)
    assert b'User registered successfully!' in response.data
    user = User.query.filter_by(email='john.doe@example.com').first()
    assert user is not None

def test_register_invalid_email(client):
    response = client.post('/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@com',
        'phone': '1234567890',
        'password': 'Password123!',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'CA',
        'zip_code': '12345',
        'country': 'USA',
        'area': 'IT',
        'group': 'Development',
        'department': 'Software'
    }, follow_redirects=True)
    assert b'Invalid email format.' in response.data

def test_register_duplicate_email(client):
    user = User(
        first_name='Jane',
        last_name='Doe',
        email='jane.doe@example.com',
        phone='1234567890'
    )
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    response = client.post('/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'password': 'Password123!',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'CA',
        'zip_code': '12345',
        'country': 'USA',
        'area': 'IT',
        'group': 'Development',
        'department': 'Software'
    }, follow_redirects=True)
    assert b'Email already registered.' in response.data

def test_register_invalid_phone(client):
    response = client.post('/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@com',
        'phone': '1234567890',
        'password': 'Password123!',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'CA',
        'zip_code': '12345',
        'country': 'USA',
        'area': 'IT',
        'group': 'Development',
        'department': 'Software'
    }, follow_redirects=True)
    assert b'Invalid phone format.' in response.data

def test_register_duplicate_phone(client):
    user = User(
        first_name='Jane',
        last_name='Doe',
        email='jane.doe@example.com',
        phone='1234567890'
    )
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    response = client.post('/register', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'password': 'Password123!',
        'address': '123 Main St',
        'city': 'Anytown',
        'state': 'CA',
        'zip_code': '12345',
        'country': 'USA',
        'area': 'IT',
        'group': 'Development',
        'department': 'Software'
    }, follow_redirects=True)
    assert b'Phone already registered.' in response.data

def test_profile_update(client):
    user = User(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890'
    )
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/profile/{user.id}', data={
        'first_name': 'John',
        'last_name': 'Smith',
        'phone': '1234567890',
        'address': '456 Elm St',
        'city': 'Othertown',
        'state': 'NY',
        'zip_code': '54321',
        'country': 'USA',
        'area': 'HR',
        'group': 'Recruitment',
        'department': 'Hiring'
    }, follow_redirects=True)
    assert b'Profile updated successfully' in response.data
    user = User.query.get(user.id)
    assert user.last_name == 'Smith'
    assert user.address == '456 Elm St'

def test_delete_user(client):
    user = User(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890'
    )
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/admin/delete/{user.id}', follow_redirects=True)
    assert b'User deleted successfully' in response.data
    user = User.query.get(user.id)
    assert user is None
