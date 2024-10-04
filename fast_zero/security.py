from datetime import datetime, timedelta

from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

SERCET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Lets protect the user password
pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    # receve the password and trasnform into a hash
    return pwd_context.hash(password)


def verify_password(plain_password: str, hased_password: str):
    # verify with the password is equals to the hash version
    return pwd_context.verify(plain_password, hased_password)


def create_access_token(data_payload: dict):
    to_encode = data_payload.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, SERCET_KEY, algorithm=ALGORITHM)
    return encode_jwt
