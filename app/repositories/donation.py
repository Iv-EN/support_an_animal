from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation
from app.repositories.base import BaseRepository


class DonationRepository(BaseRepository[Donation]):
    async def get_user_donations(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Donation]:
        query = select(Donation).where(Donation.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()


donation_crud = DonationRepository(Donation)
