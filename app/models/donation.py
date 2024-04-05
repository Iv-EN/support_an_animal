from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    """Модель для пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)