from pwdlib import PasswordHash

# Lets protect the user password
pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    # receve the password and trasnform into a hash
    return pwd_context.hash(password)


def verify_password(plain_password: str, hased_password: str):
    # verify with the password is equals to the hash version
    return pwd_context.verify(plain_password, hased_password)
