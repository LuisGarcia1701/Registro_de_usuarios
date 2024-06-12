import pytest
from models import User
from werkzeug.security import generate_password_hash

def test_set_password():
    user = User(first_name='John', last_name='Doe', email='john.doe@example.com')
    user.set_password('Password123!')
    assert user.password_hash != 'Password123!'
    assert user.check_password('Password123!') is True

def test_check_password():
    user = User(first_name='John', last_name='Doe', email='john.doe@example.com')
    user.password_hash = generate_password_hash('Password123!')
    assert user.check_password('Password123!') is True
    assert user.check_password('WrongPassword') is False
