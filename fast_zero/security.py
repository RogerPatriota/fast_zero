from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import Select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

# Lets protect the user password
pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

settings = Settings()


def get_password_hash(password: str):
    # receve the password and trasnform into a hash
    return pwd_context.hash(password)


def verify_password(plain_password: str, hased_password: str):
    # verify with the password is equals to the hash version
    return pwd_context.verify(plain_password, hased_password)


def create_access_token(data_payload: dict):
    to_encode = data_payload.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encode_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credential_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
    except DecodeError:
        raise credential_exception
    except ExpiredSignatureError:
        raise credential_exception

    user_db = session.scalar(Select(User).where(User.email == username))

    return user_db
