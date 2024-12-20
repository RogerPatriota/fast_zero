from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'User name or email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': f'r{other_user.username}',
            'email': f'r{other_user.email}',
            'password': f'r{other_user.clean_password}',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': f'r{other_user.username}',
        'email': f'r{other_user.email}',
        'id': user.id,
    }


def test_not_update_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Lucas',
            'email': 'lucassantos@gmail.com',
            'password': 'secret2',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_not_update_same_user(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': f'{other_user.username}',
            'email': f'{other_user.email}',
            'password': f'{other_user.clean_password}',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'User name or email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'message': 'User deleted'}


def test_not_delete_user(client, other_user, token):
    response = client.delete(
        f'users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'detail': 'Not enough permission'}
