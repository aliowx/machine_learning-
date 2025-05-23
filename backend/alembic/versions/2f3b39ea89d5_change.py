"""change

Revision ID: 2f3b39ea89d5
Revises: b3fcd4b9ff49
Create Date: 2025-05-19 06:13:48.485050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f3b39ea89d5'
down_revision: Union[str, None] = 'b3fcd4b9ff49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('processedfile', 'result',
                    existing_type=sa.String(),
                    type_=sa.JSON(),
                    existing_nullable=True,
                    postgresql_using='result::json')

def downgrade():
    op.alter_column('processedfile', 'result',
                    existing_type=sa.JSON(),
                    type_=sa.String(),
                    existing_nullable=True)