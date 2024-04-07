from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        donations = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
