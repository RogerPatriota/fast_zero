from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clen_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_not_get_token(client):
    response = client.post(
        'auth/token', data={'username': 'roge', 'password': '234'}
    )

    token = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}
