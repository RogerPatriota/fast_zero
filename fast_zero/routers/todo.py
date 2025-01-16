from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    Message,
    TodoFilter,
    TodoList,
    TodoPatch,
    TodoPublic,
    TodoPublicPatch,
    TodoSchema,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todo', tags=['To-do'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Filter = Annotated[TodoFilter, Query()]


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
def read_todos(
    session: T_Session,
    current_user: T_CurrentUser,
    todo_filter: Annotated[TodoFilter, Query()],
):
    todo_query = select(Todo).where(Todo.user_id == current_user.id)

    # check if any filter was send with the endp (title...)
    # if so, add to the db query
    if todo_filter.title:
        todo_query = todo_query.filter(Todo.title.contains(todo_filter.title))
    if todo_filter.description:
        todo_query = todo_query.filter(Todo.description.contains(todo_filter.description))
    if todo_filter.state:
        todo_query = todo_query.filter(Todo.state == todo_filter.state)

    todos = session.scalars(
        todo_query.offset(todo_filter.offset).limit(todo_filter.limit)
    ).all()

    return {'todos': todos}


@router.post('/', response_model=TodoPublic)
def create_todo(session: T_Session, current_user: T_CurrentUser, todo: TodoSchema):
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


@router.patch('/{todo_id}', response_model=TodoPublicPatch, status_code=HTTPStatus.OK)
def update_todo(
    session: T_Session,
    current_user: T_CurrentUser,
    todo: TodoPatch,
    todo_id: int,
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')
    # the model take the schema an change to a json(dump)
    # the exclude, see what keys was not send in the payload
    # with only the field(k) and the new data(v)
    # the setattr change into the db_todo(database)
    for k, v in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, k, v)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message, status_code=HTTPStatus.OK)
def delete_todo(session: T_Session, current_user: T_CurrentUser, todo_id: int):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    )

    if not db_todo:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Not found or do not has enough permission to delete',
        )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Task deleted'}
