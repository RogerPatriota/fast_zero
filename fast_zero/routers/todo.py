from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import TodoFilter, TodoList, TodoPublic, TodoSchema
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todo', tags=['To-do'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Filter = Annotated[TodoFilter, Query()]


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
def read_todos(
    session: T_Session,
    current_user: T_CurrentUser,
    todo_filter: T_Filter,
):
    todo_query = select(Todo).where(Todo.user_id == current_user.id)

    if todo_filter.title:
        todo_query = todo_query.filter(Todo.title.contains(todo_filter.title))
    if todo_filter.description:
        todo_query = todo_query.filter(
            Todo.description.contains(todo_filter.description)
        )
    if todo_filter.state:
        todo_query = todo_query.filter(Todo.state == todo_filter.state)

    todos = session.scalars(
        todo_query.offset(todo_filter.offset).limit(todo_filter.limit)
    ).all()

    return {'todos': todos}


@router.post('/', response_model=TodoPublic)
def create_todo(
    session: T_Session, current_user: T_CurrentUser, todo: TodoSchema
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=current_user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
