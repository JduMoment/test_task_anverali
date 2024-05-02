from datetime import datetime

import bcrypt
from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from flask_login import UserMixin

from test_task_anverali.db import ModelBase

user_space_type = ENUM(
    'executor', 'customer',
    name='user_space_type_enum',
)


class User(ModelBase, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    space_type: Mapped[str] = mapped_column(type_=user_space_type, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    salt: Mapped[str] = mapped_column(nullable=False)
    hash_password: Mapped[str] = mapped_column(nullable=False)
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

    def check_pwd(self, password):
        return self.hash_password == bcrypt.hashpw(password.encode(), self.salt.encode()).decode()

    @staticmethod
    def hash_pwd(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt), salt

    def has_one_of_role(self, role_names):
        return any(role.role.name in role_names for role in self.roles)


class UserRole(ModelBase):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('roles.id', ondelete='CASCADE'), unique=True)

    user = relationship('User', back_populates='roles', foreign_keys=[user_id])
    role = relationship('Role', back_populates='users', foreign_keys=[role_id])

    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
    )
