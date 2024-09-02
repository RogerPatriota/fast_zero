from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
            'email': 'roger.santos@global.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Roger',
        'email': 'roger.santos@global.com',
        'id': 1,
    }


def test_create_same_user(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'senha',
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
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


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


def test_not_delete_user(client):
    response = client.delete('users/4')
    assert response.json() == {'detail': 'User not found'}
