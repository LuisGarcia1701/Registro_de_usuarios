import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def browser():
    driver = webdriver.Safari()
    yield driver
    driver.quit()


def test_register_user(browser):
    browser.get('http://127.0.0.1:5000/register')

    browser.find_element(By.NAME, 'first_name').send_keys('John')
    browser.find_element(By.NAME, 'last_name').send_keys('Doe')
    browser.find_element(By.NAME, 'email').send_keys('john.doe@example.com')
    browser.find_element(By.NAME, 'phone').send_keys('1234567890')
    browser.find_element(By.NAME, 'password').send_keys('Password123!')
    browser.find_element(By.NAME, 'address').send_keys('123 Main St')
    browser.find_element(By.NAME, 'city').send_keys('Anytown')
    browser.find_element(By.NAME, 'state').send_keys('CA')
    browser.find_element(By.NAME, 'zip_code').send_keys('12345')
    browser.find_element(By.NAME, 'country').send_keys('USA')
    browser.find_element(By.NAME, 'area').send_keys('IT')
    browser.find_element(By.NAME, 'group').send_keys('Development')
    browser.find_element(By.NAME, 'department').send_keys('Software')
    browser.find_element(By.TAG_NAME, 'button').click()

    assert 'User registered successfully!' in browser.page_source


def test_invalid_email_register(browser):
    browser.get('http://127.0.0.1:5000/register')

    browser.find_element(By.NAME, 'first_name').send_keys('John')
    browser.find_element(By.NAME, 'last_name').send_keys('Doe')
    browser.find_element(By.NAME, 'email').send_keys('john.doe@com')
    browser.find_element(By.NAME, 'password').send_keys('Password123!')
    browser.find_element(By.NAME, 'phone').send_keys('1234567890')
    browser.find_element(By.NAME, 'address').send_keys('123 Main St')
    browser.find_element(By.NAME, 'city').send_keys('Anytown')
    browser.find_element(By.NAME, 'state').send_keys('CA')
    browser.find_element(By.NAME, 'zip_code').send_keys('12345')
    browser.find_element(By.NAME, 'country').send_keys('USA')
    browser.find_element(By.NAME, 'area').send_keys('IT')
    browser.find_element(By.NAME, 'group').send_keys('Development')
    browser.find_element(By.NAME, 'department').send_keys('Software')
    browser.find_element(By.TAG_NAME, 'button').click()

    assert 'Invalid email format.' in browser.page_source


def test_duplicate_email_register(browser):
    # Pre-register a user
    browser.get('http://127.0.0.1:5000/register')

    browser.find_element(By.NAME, 'first_name').send_keys('Jane')
    browser.find_element(By.NAME, 'last_name').send_keys('Doe')
    browser.find_element(By.NAME, 'email').send_keys('jane.doe@example.com')
    browser.find_element(By.NAME, 'password').send_keys('Password123!')
    browser.find_element(By.NAME, 'phone').send_keys('1234567890')
    browser.find_element(By.NAME, 'address').send_keys('123 Main St')
    browser.find_element(By.NAME, 'city').send_keys('Anytown')
    browser.find_element(By.NAME, 'state').send_keys('CA')
    browser.find_element(By.NAME, 'zip_code').send_keys('12345')
    browser.find_element(By.NAME, 'country').send_keys('USA')
    browser.find_element(By.NAME, 'area').send_keys('IT')
    browser.find_element(By.NAME, 'group').send_keys('Development')
    browser.find_element(By.NAME, 'department').send_keys('Software')
    browser.find_element(By.TAG_NAME, 'button').click()

    # Try to register the same email again
    browser.get('http://127.0.0.1:5000/register')

    browser.find_element(By.NAME, 'first_name').send_keys('John')
    browser.find_element(By.NAME, 'last_name').send_keys('Doe')
    browser.find_element(By.NAME, 'email').send_keys('jane.doe@example.com')
    browser.find_element(By.NAME, 'phone').send_keys('1234567890')
    browser.find_element(By.NAME, 'password').send_keys('Password123!')
    browser.find_element(By.NAME, 'address').send_keys('123 Main St')
    browser.find_element(By.NAME, 'city').send_keys('Anytown')
    browser.find_element(By.NAME, 'state').send_keys('CA')
    browser.find_element(By.NAME, 'zip_code').send_keys('12345')
    browser.find_element(By.NAME, 'country').send_keys('USA')
    browser.find_element(By.NAME, 'area').send_keys('IT')
    browser.find_element(By.NAME, 'group').send_keys('Development')
    browser.find_element(By.NAME, 'department').send_keys('Software')
    browser.find_element(By.TAG_NAME, 'button').click()

    assert 'Email already registered.' in browser.page_source


def test_profile_update(browser):
    # Pre-register a user
    browser.get('http://127.0.0.1:5000/register')

    browser.find_element(By.NAME, 'first_name').send_keys('John')
    browser.find_element(By.NAME, 'last_name').send_keys('Doe')
    browser.find_element(By.NAME, 'email').send_keys('john.doe@example.com')
    browser.find_element(By.NAME, 'phone').send_keys('1234567890')
    browser.find_element(By.NAME, 'password').send_keys('Password123!')
    browser.find_element(By.NAME, 'address').send_keys('123 Main St')
    browser.find_element(By.NAME, 'city').send_keys('Anytown')
    browser.find_element(By.NAME, 'state').send_keys('CA')
    browser.find_element(By.NAME, 'zip_code').send_keys('12345')
    browser.find_element(By.NAME, 'country').send_keys('USA')
    browser.find_element(By.NAME, 'area').send_keys('IT')
    browser.find_element(By.NAME, 'group').send_keys('Development')
    browser.find_element(By.NAME, 'department').send_keys('Software')
    browser.find_element(By.TAG_NAME, 'button').click()

    # Log in as the user
    browser.get('http://127.0.0.1:5000/login')
    browser.find_element(By.NAME, 'email').send_keys('john.doe@example.com')
    browser.find_element(By.NAME, 'password').send_keys('Password123!')
    browser.find_element(By.TAG_NAME, 'button').click()

    # Update profile
    browser.get('http://127.0.0.1:5000/profile/1')
    browser.find_element(By.NAME, 'last_name').clear()
    browser.find_element(By.NAME, 'last_name').send_keys('Smith')
    browser.find_element(By.NAME, 'address').clear()
    browser.find_element(By.NAME, 'address').send_keys('456 Elm St')
    browser.find_element(By.TAG_NAME, 'button').click()

    assert 'Profile updated successfully' in browser.page_source
    assert 'Smith' in browser.find_element(By.NAME, 'last_name').get_attribute('value')
    assert '456 Elm St' in browser.find_element(By.NAME, 'address').get_attribute('value')
