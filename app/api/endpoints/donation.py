from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationDBSuperUser,
)
from app.services.investing import invest

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBSuperUser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Getting a list of all donations (super users only)",
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Возвращает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary="Getting a list of current user donations"
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_user_donations(
        user,
        session
    )


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary="Creating a new donation by user"
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation_in, session, user)
    await invest(session)
    await session.refresh(new_donation)
    return new_donation
