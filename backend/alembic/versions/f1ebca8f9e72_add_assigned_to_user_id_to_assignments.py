"""add_assigned_to_user_id_to_assignments

Revision ID: f1ebca8f9e72
Revises: 1959f8f623ea
Create Date: 2026-01-27 15:46:40.372744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1ebca8f9e72'
down_revision: Union[str, None] = '1959f8f623ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
