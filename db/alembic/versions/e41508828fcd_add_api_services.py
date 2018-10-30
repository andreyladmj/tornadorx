"""add_api_services

Revision ID: e41508828fcd
Revises: 729393f76033
Create Date: 2018-09-21 12:07:13.813927

"""

# revision identifiers, used by Alembic.
from edusson_ds_main.db.models import ApiService
from sqlalchemy import insert, delete
from sqlalchemy.orm import Session

revision = 'e41508828fcd'
down_revision = '729393f76033'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    connection = op.get_bind()
    session = Session(bind=connection)
    session.execute(insert(ApiService, values={ApiService.name: "place2paid-prediction"}))
    session.commit()


def downgrade():
    connection = op.get_bind()
    session = Session(bind=connection)
    session.query(ApiService).filter_by(name="place2paid-prediction").delete()
    session.commit()
