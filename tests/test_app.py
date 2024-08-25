from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)  # arrange - Set up the object to be tested


def test_root_app(client):
    response = client.get('/')  # act - Act on the object (simulate a request)

    # assert - Making declarations(what you expected) about the object (status)
    assert response.status_code == HTTPStatus.OK
    # assert - Making declarations about the object (response)
    assert response.json() == {'message': 'Hello World!!'}


def test_create_user(client):
    response = client.post(
        '/users',  # url
        json={  # body
            'username': 'Roger',
            'email': 'roger.santos@gmail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Roger',
        'email': 'roger.santos@gmail.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Lucas',
            'email': 'lucassantos@gmail.com',
            'password': 'senha',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Lucas',
        'email': 'lucassantos@gmail.com',
        'id': 1,
    }


def test_not_update_user(client):
    response = client.put(
        '/users/5',
        json={
            'username': 'Lucas',
            'email': 'lucassantos@gmail.com',
            'password': 'secret2',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_not_delete_user(client):
    response = client.delete('users/4')

    assert response.json() == {'detail': 'User not found'}
