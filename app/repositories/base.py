from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    """Базовый набор стандартных CRUD-методов."""

    def __init__(self, model: Type[T]) -> None:
        self.model = model

    async def get(self, obj_id: int, db_session: AsyncSession) -> Optional[T]:
        """Получает объект по id."""
        query = select(self.model).where(self.model.id == obj_id)
        result = await db_session.execute(query)
        return result.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[T]:
        """Получает все объекты класса."""
        query = select(self.model)
        result = await session.execute(query)
        return result.scalars().all()

    async def create(self, obj_in_data: dict, session: AsyncSession) -> T:
        """Создаёт новый объект."""
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_not_closed_objects(self, session: AsyncSession) -> List:
        """Получает все незакрытые проекты и сортирует их по дате создания."""
        not_closed_obj = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return not_closed_obj.scalars().all()

    async def update(self, db_obj: T, obj_in: dict, session: AsyncSession) -> T:
        """Обновляет объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: int) -> int:
        """Удаляет объект."""
        query = select(self.model).where(self.model.id == id)
        result = await session.execute(query)
        db_obj = result.scalars().first()
        await session.delete(db_obj)
        await session.commit()

        return id
