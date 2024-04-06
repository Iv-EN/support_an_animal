from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Базовый класс Pydantic-модели."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Pidantic-модель для создания благотворительного проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Pidantic-модель для обновления благотворительного проекта."""

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value

    @validator('description')
    def description_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Описание не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    """Pidantic-схема для описания объекта."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True