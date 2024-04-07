from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_before_delete,
    check_charity_project_before_edit,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import invest

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Creating a new charity project (super users only)",
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await invest(session)
    await session.refresh(new_charity_project)

    return new_charity_project


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Getting a list of all charitable projects",
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Charity project data update (super users only)",
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;
     нельзя установить требуемую сумму меньше уже вложенной."""

    charity_project_db = await check_charity_project_before_edit(
        project_id, charity_project_in, session
    )
    charity_project = await charity_project_crud.update(
        charity_project_db, charity_project_in, session
    )
    return charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Deleting a charity project (super users only)",
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    charity_project = await check_charity_project_before_delete(
        project_id, session
    )
    charity_project = await charity_project_crud.delete(
        charity_project, session
    )
    return charity_project
