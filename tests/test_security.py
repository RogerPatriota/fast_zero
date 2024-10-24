from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SERCET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, SERCET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
