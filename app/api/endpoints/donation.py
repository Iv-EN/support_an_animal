from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationDB,
                                  DonationDBSuperUser)
from app.services.investing import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperUser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session=session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для авторизованных пользователей."""
    return await donation_crud.get_user_donations(
        session=session,
        user=user
    )


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для авторизированных пользователей."""
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await invest(session=session)
    await session.refresh(new_donation)
    return new_donation