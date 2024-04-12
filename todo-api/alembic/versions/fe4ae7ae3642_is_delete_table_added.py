"""is_delete table added 

Revision ID: fe4ae7ae3642
Revises: 9443fa1bd291
Create Date: 2024-04-12 14:46:51.437726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe4ae7ae3642'
down_revision: Union[str, None] = '9443fa1bd291'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_delete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_delete')
    # ### end Alembic commands ###
