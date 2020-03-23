import pytest
from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True


@pytest.fixture(scope='module')
def client():
    flask_app = create_app(TestConfig)
    return flask_app.test_client()


def test_home_page(client):
    response = client.get('/')
    response_index = client.get('/index')
    assert response.status_code == 200
    assert response_index.status_code == 200


def test_linkedin_profile(client):
    response = client.get('/linkedin_profile')
    assert response.status_code == 302  # redirection


def test_oslo_byssykkel(client):
    response = client.get('/oslo_byssykkel')
    assert response.status_code == 302  # redirection