from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def close_fully_invested_object(obj: Union[CharityProject, Donation]) -> None:
    """Закрывает полностью инвестированный проект."""
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def invest(session: AsyncSession):
    """Распределяет доступную сумму пожертвований по открытым проектам."""
    investments_open = await donation_crud.get_not_closed_objects(
        session=session
    )
    unclosed_projects = await charity_project_crud.get_not_closed_objects(
        session=session
    )
    if not investments_open or not unclosed_projects:
        return
    for donation in investments_open:
        for project in unclosed_projects:
            required_amount = project.full_amount - project.invested_amount
            amount_available_donation = (
                donation.full_amount - donation.invested_amount
            )
            needed_money = required_amount - amount_available_donation
            if needed_money == 0:
                close_fully_invested_object(donation)
                close_fully_invested_object(project)
            if needed_money < 0:
                donation.invested_amount += abs(needed_money)
                close_fully_invested_object(donation)
            if needed_money > 0:
                project.invested_amount += amount_available_donation
                close_fully_invested_object(donation)
        await session.commit()
