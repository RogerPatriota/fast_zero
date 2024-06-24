from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

database = []

app = FastAPI()


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Hello World!!'}


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    user_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_id)

    return user_id
