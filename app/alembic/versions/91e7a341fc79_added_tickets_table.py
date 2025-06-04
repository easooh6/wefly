"""added tickets table

Revision ID: 91e7a341fc79
Revises: bf7bca821ce2
Create Date: 2025-06-03 17:53:13.785021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91e7a341fc79'
down_revision: Union[str, None] = 'bf7bca821ce2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
