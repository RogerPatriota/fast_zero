from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, todo, user
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Hello World!!'}
