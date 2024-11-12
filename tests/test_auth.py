from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_not_get_token(client, other_user):
    response = client.post(
        'auth/token',
        data={'username': f'{other_user.id}', 'password': f'{other_user.id}'},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}


def test_not_get_token_wrong_password(client, user, other_user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': other_user.password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}


def test_token_expired(client, user, other_user):
    with freeze_time('2024-11-11 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    with freeze_time('2024-11-11 12:31:00'):
        response = client.put(
            f'users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': other_user.username,
                'email': other_user.email,
                'password': other_user.password,
            },
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, user, token):
    response = client.post(
        'auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    new_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in new_token
    assert 'token_type' in new_token
    # assert new_token['access_token'] != token


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
