from datetime import datetime

from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from flask_login import UserMixin

from test_task_anverali.db import ModelBase

user_space_type = ENUM(
    'executor', 'customer', 'admin',
    name='user_space_type_enum',
)


class User(ModelBase, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    space_type: Mapped[str] = mapped_column(type_=user_space_type, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    phone_number: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )

    roles = relationship('UserRole', back_populates='user')

    def __str__(self):
        return self.email

    __table_args__ = (Index('index_id_user', id),)


class UserRole(ModelBase):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('roles.id', ondelete='CASCADE'), unique=True)

    user = relationship('User', back_populates='roles', foreign_keys=[user_id])
    role = relationship('Role', back_populates='users', foreign_keys=[role_id])

    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
        Index('index_id_user_role', id, role_id),
    )

