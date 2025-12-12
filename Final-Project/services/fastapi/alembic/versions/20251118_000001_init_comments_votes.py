"""init comments votes

Revision ID: 20251118_000001
Revises: 
Create Date: 2025-11-18 00:00:01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251118_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User table (minimal subset)
    op.create_table(
        'User',
        sa.Column('user_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(length=255)),
        sa.Column('password_hash', sa.String(length=255)),
        sa.Column('first_name', sa.String(length=100)),
        sa.Column('last_name', sa.String(length=100)),
        sa.Column('is_enabled', sa.Boolean(), server_default=sa.text('0')),
    )

    # Startup table (minimal subset)
    op.create_table(
        'Startup',
        sa.Column('startup_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255)),
        sa.Column('owner_user_id', sa.Integer()),
        sa.Column('category_id', sa.Integer()),
        sa.ForeignKeyConstraint(['owner_user_id'], ['User.user_id'], ondelete='CASCADE'),
    )

    # Comment table
    op.create_table(
        'Comment',
        sa.Column('comment_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('modified_date', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('startup_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['User.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['startup_id'], ['Startup.startup_id'], ondelete='CASCADE'),
    )

    # Vote table
    op.create_table(
        'Vote',
        sa.Column('vote_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('vote_type', sa.Enum('upvote', 'downvote', name='votetype'), nullable=False),
        sa.Column('created_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('startup_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['User.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['startup_id'], ['Startup.startup_id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'startup_id', name='unique_vote_per_user_startup'),
    )


def downgrade() -> None:
    op.drop_table('Vote')
    op.drop_table('Comment')
    op.drop_table('Startup')
    op.drop_table('User')
