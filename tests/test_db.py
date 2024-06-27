from sqlalchemy import select

from fast_zero.models import User
from tests.confitest import session


def test_create_user(session: session):
    new_user = User(username='Roger', password='secret', email='test@test')
    session.add(new_user)
    session.commit()

    result = session.scalar(select(User).where(User.username == 'Roger'))
    # session.scalar == Transform the db response into a Python Object

    assert result.id == 1
