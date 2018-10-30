"""fix dash auth table

Revision ID: bf16711d3434
Revises: 36408fac1ba1
Create Date: 2018-10-03 12:59:06.070846

"""

# revision identifiers, used by Alembic.
revision = 'bf16711d3434'
down_revision = '36408fac1ba1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYINT


def upgrade():
    with op.batch_alter_table("dash_user") as batch_op:
        batch_op.drop_column('is_active')
        batch_op.drop_column('session_token')
        batch_op.drop_column('password_user')
        batch_op.add_column(sa.Column('is_active', TINYINT(unsigned=True), nullable=False, default=True))


def downgrade():
    with op.batch_alter_table("dash_user") as batch_op:
        batch_op.add_column(sa.Column('password_user', sa.String(255), nullable=True))
        batch_op.add_column(sa.Column('session_token', sa.String(255), nullable=True))
