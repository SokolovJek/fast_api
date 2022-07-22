from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import status, HTTPException
from jose import JWTError, jwt

from db.session import get_db
from core.hashing import Hasher
from schemas.tokens import Token
from db.repository.login import get_user
from core.security import create_access_token
from core.config import settings

router = APIRouter()


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    print("authenticate_user =====", user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    функция для аутентификации пользователя и выдачи ему токена
    :param form_data: данные полученые с формы
    :param db: обьект БД
    :return: ответ на запрос
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Некоректный логин или пароль',
        )
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expire
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/token')


def get_current_user_form_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Она работает как зависимость,
    создадим зависимость для идентификации current_user.
    :param token: токен
    :param db: объект БД
    :return: объект пользователя
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Не удалось подтвердить учетные данные')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user
