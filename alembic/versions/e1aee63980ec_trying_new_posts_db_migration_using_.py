"""trying new posts db migration using alembic

Revision ID: e1aee63980ec
Revises: 
Create Date: 2024-04-22 18:59:41.052722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1aee63980ec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('postsUsingAlembic',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('postTitle',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('postsUsingAlembic')
    pass
