from .base import Base
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, Integer
from datetime import datetime

class RefreshToken(Base):

    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.id'))
    token_hash: Mapped[str] = mapped_column(String(255))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")