from http import HTTPStatus


def test_root_app(client):
    response = client.get('/')  # act - Act on the object (simulate a request)

    # assert - Making declarations(what you expected) about the object (status)
    assert response.status_code == HTTPStatus.OK
    # assert - Making declarations about the object (response)
    assert response.json() == {'message': 'Hello World!!!'}
