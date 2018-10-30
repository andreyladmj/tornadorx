"""dash_user_board_view_log

Revision ID: 36408fac1ba1
Revises: e41508828fcd
Create Date: 2018-09-21 15:58:14.873682

"""
from datetime import datetime

from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYINT

# revision identifiers, used by Alembic.
revision = '36408fac1ba1'
down_revision = 'e41508828fcd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'dash_user_board_view_log',
        sa.Column('id', Integer(unsigned=True), primary_key=True),
        sa.Column('user_id', Integer(unsigned=True), nullable=True),
        sa.Column('args', sa.Text(), nullable=True),
        sa.Column('dashboard_id', TINYINT(unsigned=True), nullable=True),
        sa.Column('board_name', sa.String(255), nullable=False),
        sa.Column('date_view', sa.DateTime, nullable=False, default=datetime.now()),
    )

    op.create_foreign_key(
        'fk_dash_user_board_view_log_dash_dashboard',
        'dash_user_board_view_log', 'dash_dashboard',
        ['dashboard_id'], ['dashboard_id'],
    )


def downgrade():
    op.drop_table('dash_user_board_view_log')
