from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    """Проверяет название проекта на уникальность."""
    charity_project = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!"
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверяет наличие проекта."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Проект не найден!"
        )
    return charity_project


async def check_charity_project_before_edit(
    project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Проверяет проект для редактирования."""
    charity_project = await check_charity_project_exists(
        project_id=project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!"
        )

    new_full_amount = charity_project_in.full_amount
    if new_full_amount and charity_project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя установить ребуемую сумму меньше уже вложенной"
        )
    new_name = charity_project_in.name
    await check_name_duplicate(new_name, session)
    return charity_project


async def check_charity_project_before_delete(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверяет проект для удаления."""
    charity_project = await check_charity_project_exists(project_id, session)

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!"
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя удалить!"
        )
    return charity_project
