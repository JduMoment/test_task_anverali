"""init

Revision ID: 2ed33cefed12
Revises:
Create Date: 2024-05-01 10:36:22.996704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql

from test_task_anverali.models import (User, Role, UserRole,
                                       UserExecutorsSettings)

# revision identifiers, used by Alembic.
revision: str = '2ed33cefed12'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('space_type', postgresql.ENUM('executor', 'customer', name='user_space_type_enum'), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('salt', sa.String(), nullable=False),
    sa.Column('hash_password', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('customer_settings',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('about_me', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('executor_settings',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('experience', sa.String(), nullable=True),
    sa.Column('about_me', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('user_roles',
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('role_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role_id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    hash_password, salt = User.hash_pwd('321321')
    user = session.execute(sa.insert(User).values(
        email='curagin.vanya@yandex.ru',
        hash_password=hash_password.decode(),
        salt=salt.decode(),
        first_name='Vanya',
        last_name='Curagin',
        space_type='executor',
        phone_number='+79063511583'
    ))
    user_id = user.inserted_primary_key[0]

    result = session.execute(sa.insert(Role).values(
        name='admin'
    ))
    role_id = result.inserted_primary_key[0]

    op.execute(
        sa.insert(UserRole).values(
            user_id=user_id,
            role_id=role_id
        )
    )

    op.execute(sa.insert(UserExecutorsSettings).values(
        user_id=user_id,
        experience='some experience',
        about_me='some about me'
    ))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('executor_settings')
    op.drop_table('customer_settings')
    op.drop_table('users')
    op.drop_table('roles')
    op.execute(
        """
        DROP TYPE user_space_type_enum;
        """
    )
    # ### end Alembic commands ###
