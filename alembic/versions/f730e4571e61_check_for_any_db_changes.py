"""check for any db changes

Revision ID: f730e4571e61
Revises: 572ec60a9604
Create Date: 2025-08-29 08:32:19.088647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f730e4571e61'
down_revision: Union[str, None] = '572ec60a9604'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
