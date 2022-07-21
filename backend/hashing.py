from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hasher:
    """Здесь будет логика создания хеша из пароля и сравнивания паролей"""

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Сравнивает пароль и хэш
        :param plain_password: пароль
        :param hashed_password: хэш-пароля
        :return: boolean
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """
        Выдает хэш из переданного в метод пароля
        :param password: пароль
        :return: хэш из пароля
        """
        return pwd_context.hash(password)


a = Hasher.get_password_hash('master')
print(a)

print(Hasher.verify_password('master', a))
