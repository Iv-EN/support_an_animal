from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    """Создать новое пожертвование."""
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate):
    """Описывает объект для зарегестрированного пользователя."""
    id: int
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDBSuperUser(DonationDB):
    """Описывает объект для СуперЮзера."""
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
