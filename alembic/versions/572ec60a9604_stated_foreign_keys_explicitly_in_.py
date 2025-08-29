"""stated foreign keys explicitly in relationships

Revision ID: 572ec60a9604
Revises: 8428ce5238d1
Create Date: 2025-08-28 16:35:25.046635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '572ec60a9604'
down_revision: Union[str, None] = '8428ce5238d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
