from sqlalchemy import BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from test_task_anverali.db import ModelBase


class Role(ModelBase):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    users = relationship('UserRole', back_populates='role')

    def __str__(self):
        return self.role

    __table_args__ = (Index('index_id_role', id),)
