from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_app():
    client = TestClient(app) #arrange - Set up the object to be tested

    response = client.get('/') #act - Act on the object

    #assert - Making declarations about the object (status)
    assert response.status_code == HTTPStatus.OK
    #assert - Making declarations about the object (response)
    assert response.json() == {'message': 'Hello World!!'}
