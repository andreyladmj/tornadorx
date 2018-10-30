"""Initial state

Revision ID: cd3bd1b878ca
Revises: 
Create Date: 2018-08-21 16:11:44.345246

"""

# revision identifiers, used by Alembic.
revision = 'cd3bd1b878ca'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_ds_orders_backup_order_id'), 'ds_orders_backup', ['order_id'], unique=False)
    op.drop_index('ix_ds_orders_order_id', table_name='ds_orders_backup')
    op.drop_index('ix_ds_retention_weights_timeseries_date_bin_period_upper_af3c',
                  table_name='ds_retention_weights_timeseries')
    op.create_index(op.f('ix_ds_writers_backup_writer_id'), 'ds_writers_backup', ['writer_id'], unique=False)
    op.drop_index('ix_ds_writers_writer_id', table_name='ds_writers_backup')
    op.drop_index('date_UNIQUE', table_name='st_daily_general_report')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('date_UNIQUE', 'st_daily_general_report', ['date'], unique=True)
    op.create_index('ix_ds_writers_writer_id', 'ds_writers_backup', ['writer_id'], unique=False)
    op.drop_index(op.f('ix_ds_writers_backup_writer_id'), table_name='ds_writers_backup')
    op.create_index('ix_ds_retention_weights_timeseries_date_bin_period_upper_af3c', 'ds_retention_weights_timeseries',
                    ['date_bin_period_upper_boundary'], unique=False)
    op.create_index('ix_ds_orders_order_id', 'ds_orders_backup', ['order_id'], unique=False)
    op.drop_index(op.f('ix_ds_orders_backup_order_id'), table_name='ds_orders_backup')
    # ### end Alembic commands ###
