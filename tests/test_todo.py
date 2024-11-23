
def create_todo(client, token):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'teste todo',
            'description': 'test todo description',
            'state': 'draft',
        },
    )
    # assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'teste todo',
        'description': 'test todo description',
        'state': 'draft',
    }
