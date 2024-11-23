from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todo', tags=['To-do'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
