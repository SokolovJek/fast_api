"""
Поскольку мы используем шаблон репозитория и хотим чтобы логика формы базы данных была полностью отделена от
логики маршрутов fastapi, создаем функцию «create_new_user» для логики создания user.
Сдесь хранится БИЗНЕС-ЛОГИКА
"""
from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    """
    Извлекли логику работы с БД из функции create_user(end-point '/user/'),
     для того чтоб в случае чего можно было изменить ORM
    """
    user = User(username=user.username,
                email=user.email,
                hashed_password=Hasher.get_password_hash(user.password),
                is_active=True,
                is_superuser=False
                )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
