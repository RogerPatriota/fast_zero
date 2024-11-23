from .conftest import TodoFactory


def test_read_todo_without_filter(session, client, token, user):
    expected_todos = 4
    session.bulk_save_objects(
        TodoFactory.creat_batch(expected_todos, user_id=user.id)
    )

    response = client.get('/', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == expected_todos


def test_create_todo(client, token, user):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'todo.title',
            'description': 'todo.description',
            'state': 'draft',
        },
    )
    # assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'todo.title',
        'description': 'todo.description',
        'state': 'draft',
        'id': 1,
        'user_id': user.id,
    }
