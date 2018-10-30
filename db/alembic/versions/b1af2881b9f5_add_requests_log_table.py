"""add requests log table

Revision ID: b1af2881b9f5
Revises: eb181bf6da8b
Create Date: 2018-09-11 17:06:48.040162

"""

# revision identifiers, used by Alembic.
from datetime import datetime
from sqlalchemy.dialects.mysql import INTEGER as Integer

revision = 'b1af2881b9f5'
down_revision = '0063441ef9cb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'api_request_logs',
        sa.Column('id', Integer(unsigned=True), primary_key=True),
        sa.Column('service', sa.String(50), nullable=False),
        sa.Column('user', sa.String(50), nullable=True),
        sa.Column('url', sa.String(255), nullable=False),
        sa.Column('status', Integer(unsigned=True), nullable=False),
        sa.Column('response', sa.Text, nullable=True),
        sa.Column('args', sa.Text, nullable=True),
        sa.Column('time', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.now()),
    )


def downgrade():
    op.drop_table('api_request_logs')
