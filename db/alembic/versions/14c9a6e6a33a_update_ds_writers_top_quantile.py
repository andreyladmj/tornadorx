"""update_ds_writers_top_quantile

Revision ID: 14c9a6e6a33a
Revises: db230f2f7672
Create Date: 2018-10-25 10:48:24.107698

"""

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYINT
revision = '14c9a6e6a33a'
down_revision = 'db230f2f7672'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("ds_writers", "writer_top_quantile", existing_type=TINYINT(unsigned=True), nullable=False, server_default='50')


def downgrade():
    pass
