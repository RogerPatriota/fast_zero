from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_zero.models import TodoState

# Here is the models of the responses, what the API expected from each request


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, gt=0, le=100)


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
    user_id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoFilter(FilterPage):
    title: str | None = Field(None)
    description: str = Field(None)
    state: TodoState | None = Field(None)


class TodoPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
