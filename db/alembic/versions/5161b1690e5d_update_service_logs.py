"""update_service_logs

Revision ID: 5161b1690e5d
Revises: bf16711d3434
Create Date: 2018-10-16 15:39:40.378588

"""

# revision identifiers, used by Alembic.
revision = '5161b1690e5d'
down_revision = 'bf16711d3434'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT


def upgrade():
    op.add_column('api_service_log', sa.Column('is_success', TINYINT(unsigned=True), nullable=True))
    op.add_column('api_service_log', sa.Column('request_id', sa.String(length=64), nullable=True))


def downgrade():
    with op.batch_alter_table("api_service_log") as batch_op:
        batch_op.drop_column('is_success')
        batch_op.drop_column('request_id')
