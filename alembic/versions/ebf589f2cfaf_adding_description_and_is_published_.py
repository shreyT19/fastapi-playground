"""adding description and is_published table using alembic

Revision ID: ebf589f2cfaf
Revises: e1aee63980ec
Create Date: 2024-04-22 19:12:02.742655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebf589f2cfaf'
down_revision: Union[str, None] = 'e1aee63980ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('postsUsingAlembic', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('postsUsingAlembic', 'content')
    pass
