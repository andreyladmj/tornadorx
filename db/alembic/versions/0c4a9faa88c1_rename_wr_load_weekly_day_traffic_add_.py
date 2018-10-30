"""rename wr_load_weekly_day_traffic & add bidding coeff

Revision ID: 0c4a9faa88c1
Revises: cd3bd1b878ca
Create Date: 2018-08-30 15:41:04.996370

"""

# revision identifiers, used by Alembic.
revision = '0c4a9faa88c1'
down_revision = 'cd3bd1b878ca'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('wr_load_weekly_day_traffic', 'st_system_daily_load')
    with op.batch_alter_table("st_system_daily_load") as batch_op:
        batch_op.add_column(sa.Column('bidding_coefficient', sa.Float(), nullable=True))


def downgrade():
    op.rename_table('st_system_daily_load', 'wr_load_weekly_day_traffic')
    with op.batch_alter_table("wr_load_weekly_day_traffic") as batch_op:
        batch_op.drop_column('bidding_coefficient')
