from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser[int]):
    """Базовые поля модели пользователя, кроме пароля."""


class UserCreate(BaseUserCreate):
    """Создание пользователя."""


class UserUpdate(BaseUserUpdate):
    """Обновление объекта пользователь со всеми полями, включая пароль."""