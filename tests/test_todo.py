from .conftest import TodoFactory


def test_read_todo_without_filter(session, client, token, user):
    expected_todos = 4
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id)
    )

    response = client.get(
        '/todo/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todo_with_filters(session, client, token, user, todo):

    session.bulk_save_objects(TodoFactory.create_batch(3, user_id=user.id))
    session.commit()

    response = client.get(
        f'/todo/?title={todo.title[0:8]}&description={todo.description[0:3]}&state={todo.state.value}',
        headers={'Authorization': f'Bearer {token}'},
    )
    print(response.json()['todos'])
    assert response.json()['todos'][0] == {
        'title': f'{todo.title}',
        'description': f'{todo.description}',
        'state': f'{todo.state.value}',
        'id': 1,
        'user_id': user.id,
    }


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
