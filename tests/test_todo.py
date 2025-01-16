from http import HTTPStatus

from .conftest import TodoFactory


def test_read_todo_without_filter(session, client, token, user):
    expected_todos = 4
    session.bulk_save_objects(TodoFactory.create_batch(expected_todos, user_id=user.id))

    response = client.get('/todo/', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == expected_todos


def test_read_todo_with_filters(session, client, token, user, todo):
    session.bulk_save_objects(TodoFactory.create_batch(3, user_id=user.id))
    session.commit()

    response = client.get(
        f'/todo/?title={todo.title[0:8]}&description={todo.description[0:3]}&state={todo.state.value}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 1
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


def test_update_task(client, user, token, todo):
    response = client.patch(
        f'todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'New Task'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'New Task'


def test_update_task_wrong_id(client, token):
    response = client.patch(
        'todo/10', headers={'Authorization': f'Bearer {token}'}, json={}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not found'}


def test_delete_task(client, token, todo):
    response = client.delete(
        f'todo/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task deleted'}


def test_delete_err(client, token):
    response = client.delete('todo/10', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Not found or do not has enough permission to delete'
    }
