"""added tickets table

Revision ID: 37e767585b02
Revises: 91e7a341fc79
Create Date: 2025-06-03 17:58:02.282770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e767585b02'
down_revision: Union[str, None] = '91e7a341fc79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
