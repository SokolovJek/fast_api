from sqlalchemy.orm import Session

from db.models.users import User


def get_user(username: str, db: Session):
    """
    функция для получения пользователя с БД по его email адресу
    :param username: email c формы
    :param db: обьект БД
    :return: user с БД
    """
    user = db.query(User).filter(User.email == username).first()
    return user
