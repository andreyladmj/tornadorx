"""update ds writers top quantile

Revision ID: db230f2f7672
Revises: 5161b1690e5d
Create Date: 2018-10-24 11:04:47.585381

"""

from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYINT
# revision identifiers, used by Alembic.
revision = 'db230f2f7672'
down_revision = '5161b1690e5d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("ds_writers", "writer_top_quantile", existing_type=TINYINT(unsigned=True), nullable=False)


def downgrade():
    pass
