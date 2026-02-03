"""Add RPG mechanics fields

Revision ID: 0c81906a8aa3
Revises: 
Create Date: 2026-01-25 23:22:58.833185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c81906a8aa3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add RPG fields to monsters table
    op.add_column('monsters', sa.Column('entry_cost', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('monsters', sa.Column('pass_reward', sa.Integer(), nullable=False, server_default='30'))
    op.add_column('monsters', sa.Column('fail_penalty', sa.Integer(), nullable=False, server_default='5'))
    
    # Clean up server defaults
    op.alter_column('monsters', 'entry_cost', server_default=None)
    op.alter_column('monsters', 'pass_reward', server_default=None)
    op.alter_column('monsters', 'fail_penalty', server_default=None)

    # Optional: Update gold_reward default on quests is metadata only, DB defaults usually handled by app unless set here.
    # But since we changed model default, it usually doesn't need DB schema change for default unless we enforce it.
    # We will accept that existing rows have 0.


def downgrade() -> None:
    op.drop_column('monsters', 'fail_penalty')
    op.drop_column('monsters', 'pass_reward')
    op.drop_column('monsters', 'entry_cost')
