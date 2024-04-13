from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.repositories.base import BaseRepository
from app.repositories.containers import Container


class ChatityProjectRepository(BaseRepository[CharityProject]):
    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[CharityProject]:
        """Получает проект по его названию."""
        db_project = await session.execute(
            select(CharityProject).where(CharityProject.name == project_name)
        )
        db_project = db_project.scalars().first()
        return db_project


charity_project_repository = ChatityProjectRepository(CharityProject)
