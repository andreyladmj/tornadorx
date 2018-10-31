"""udpate dashbaords

Revision ID: 2e09440e4f98
Revises: 14c9a6e6a33a
Create Date: 2018-10-29 10:09:08.953182

"""

# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey

revision = '2e09440e4f98'
down_revision = '14c9a6e6a33a'
branch_labels = None
depends_on = None

from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYINT
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


def upgrade():
    op.create_table(
        'dash_dashboard_board',
        sa.Column('board_id', TINYINT(unsigned=True), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('model_tag', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_active', TINYINT(unsigned=True), server_default='1'),
        sa.Column('date_created', sa.DateTime, server_default=func.now())
    )

    with op.batch_alter_table("dash_user_board_access") as batch_op:
        batch_op.add_column(sa.Column('board_id', TINYINT(unsigned=True), nullable=True))

    # ForeignKey('dash_dashboard_board.board_id')

    op.create_foreign_key(
        'fk_dash_user_board_access_dash_dashboard_board',
        'dash_user_board_access', 'dash_dashboard_board',
        ['board_id'], ['board_id'],
        onupdate="CASCADE", ondelete="CASCADE"
    )

    try:
        op.drop_index('user_access_UNIQUE', 'dash_user_board_access')
    except Exception:
        pass

    op.create_index('ix_user_access_board_UNIQUE', 'dash_user_board_access', ['user_id', 'dashboard_id', 'board_id'], unique=True)

    from sqlalchemy.orm import sessionmaker
    from edusson_ds_main.db.connections import DBConnectionsFacade
    from edusson_ds_main.db.models import DashDashboardBoard, DashUser
    Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
    sess = Session()

    log1 = DashDashboardBoard(name='test 1',model_tag='test 1',description='test 1')
    sess.add(log1)

    log2 = DashDashboardBoard(name='test 2',model_tag='test 2',description='test 2')
    sess.add(log2)

    log3 = DashDashboardBoard(name='test 3',model_tag='test 3',description='test 3')
    sess.add(log3)
    sess.commit()

def downgrade():
    op.drop_index('ix_user_access_board_UNIQUE', 'dash_user_board_access')

    try:
        op.create_index('user_access_UNIQUE', 'dash_user_board_access', ['user_id', 'dashboard_id'], unique=True)
    except Exception:
        pass

    op.drop_constraint(u'fk_dash_user_board_access_dash_dashboard_board', 'dash_user_board_access', type_='foreignkey')

    with op.batch_alter_table("dash_user_board_access") as batch_op:
        batch_op.drop_column('board_id')

    op.drop_table('dash_dashboard_board')
