from uuid import UUID

import typer

from core.security import get_password_hash
from dependencies.db import get_db
from models import User

users = [
    {
        "uid": UUID("f05f20a0-e52a-49a3-932a-81c81932f762"),
        "email": "admin@admin.md",
        "phone_number": "+37379911111",
        "first_name": "Admin",
        "last_name": "User",
        "is_superuser": True,
        "hashed_password": get_password_hash("252525"),
    },
]


def load_users():
    db_session = next(get_db())
    existing_users = db_session.query(User).filter(User.uid.in_([user["uid"] for user in users])).all()
    existing_users_uids = [str(existing_user.uid) for existing_user in existing_users]
    for user in users:
        db_user = User(**user)
        if str(user["uid"]) in existing_users_uids:
            db_session.merge(db_user)
        else:
            db_session.add(db_user)

    db_session.commit()


if __name__ == "__main__":
    typer.run(load_users)

