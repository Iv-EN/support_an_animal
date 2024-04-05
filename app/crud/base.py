from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Базовый набор стандартных CRUD-методов."""

    def __init__(self, model) -> None:
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession,):
        """Получает объект по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Получает все объекты класса."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession, user: Optional[User] = None):
        """Создаёт новый объект."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def get_not_closed_objects(self, session: AsyncSession):
        """Получает все незакрытые проекты и сортирует их по дате создания."""
        not_closed_obj = await session.execute(select(self.model).where(
            self.model.fully_invested.is_(False)
        ).order_by(self.model.create_date)
        )
        return not_closed_obj.scalars().all()

    async def update(self, db_obj, obj_in, session: AsyncSession,):
        """Обновляет объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def delete(self, db_obj, session: AsyncSession,):
        """Удаляет объект."""
        await session.delete(db_obj)
        await session.commit()

        return db_obj