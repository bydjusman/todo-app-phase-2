"""Initial schema migration

Revision ID: 001
Revises:
Create Date: 2026-01-02

"""
from typing import Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    # Create enum type for task priority
    op.execute("CREATE TYPE task_priority AS ENUM ('high', 'medium', 'low')")

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_superuser', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('color', sa.String(7), default='#3B82F6'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_categories_user_id', 'categories', ['user_id'])
    op.create_unique_constraint('uq_user_category_name', 'categories', ['user_id', 'name'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category_id', sa.String(36), sa.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('priority', sa.Enum('high', 'medium', 'low', name='task_priority'), default='medium', nullable=False),
        sa.Column('is_completed', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_category_id', 'tasks', ['category_id'])
    op.create_index('ix_tasks_is_completed', 'tasks', ['is_completed'])
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])


def downgrade() -> None:
    op.drop_index('ix_tasks_priority', table_name='tasks')
    op.drop_index('ix_tasks_is_completed', table_name='tasks')
    op.drop_index('ix_tasks_category_id', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')

    op.drop_unique_constraint('uq_user_category_name', 'categories', table_name='categories')
    op.drop_index('ix_categories_user_id', table_name='categories')
    op.drop_table('categories')

    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

    op.execute("DROP TYPE task_priority")
