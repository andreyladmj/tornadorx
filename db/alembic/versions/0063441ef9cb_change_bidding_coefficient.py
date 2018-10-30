"""change_bidding_coefficient

Revision ID: 0063441ef9cb
Revises: 0c4a9faa88c1
Create Date: 2018-09-06 22:07:53.670137

"""

# revision identifiers, used by Alembic.
from datetime import datetime

from sqlalchemy import update, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Session

from edusson_ds_main.db.models import StSystemDailyLoad

revision = '0063441ef9cb'
down_revision = '0c4a9faa88c1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("st_system_daily_load", "order_hour", new_column_name="hour", existing_type=TINYINT(unsigned=True), nullable=False)
    op.add_column('st_system_daily_load', sa.Column('date', sa.Date(), nullable=True))

    op.alter_column("st_system_daily_load", "paid_orders_count", existing_type=sa.Float(3,7))
    op.alter_column("st_system_daily_load", "writers_count", existing_type=sa.Float(3,7))
    op.alter_column("st_system_daily_load", "paid_orders_per_writer", existing_type=sa.Float(3,6))
    op.alter_column("st_system_daily_load", "bidding_coefficient", existing_type=sa.Float(3,5))

    connection = op.get_bind()
    session = Session(bind=connection)
    session.execute(update(StSystemDailyLoad, values={StSystemDailyLoad.date: datetime.now().date()}))
    session.commit()

    op.alter_column('st_system_daily_load', 'date', existing_type=sa.Date(), nullable=False)

    connection.execute(
        text(
            """ALTER TABLE st_system_daily_load DROP PRIMARY KEY, ADD PRIMARY KEY(date, hour);"""
        )
    )


def downgrade():
    op.alter_column("st_system_daily_load", "hour", new_column_name="order_hour", existing_type=sa.SmallInteger(),
                    nullable=False)
    op.drop_column("st_system_daily_load", "date")
