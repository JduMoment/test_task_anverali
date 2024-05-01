from sqlalchemy import ForeignKey, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from test_task_anverali.db import ModelBase


class UserExecutorsSettings(ModelBase):
    __tablename__ = 'executor_settings'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    experience: Mapped[str] = mapped_column(nullable=True)
    about_me: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (Index('index_id', id),)
