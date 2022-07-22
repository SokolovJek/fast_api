from datetime import datetime, timedelta
from typing import Optional
from jose import JOSEError, jwt

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    генерация токена JWT
    :param data: словарь с данными (sub)
    :param expires_delta: время истечения токкена
    :return: токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# jwt.decode(token, 'secret', algorithms=['HS256'])