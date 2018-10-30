"""api changes

Revision ID: 729393f76033
Revises: b1af2881b9f5
Create Date: 2018-09-12 22:18:24.276633

"""

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYINT

from edusson_ds_main.db.models import ApiUser, ApiService, ApiServiceLog

revision = '729393f76033'
down_revision = 'b1af2881b9f5'
branch_labels = None
depends_on = None

from sqlalchemy import update, text, insert, delete
from sqlalchemy.orm import Session
from alembic import op
import sqlalchemy as sa


def upgrade():
    connection = op.get_bind()
    session = Session(bind=connection)

    op.rename_table('api_request_logs', 'api_service_log')
    op.rename_table('logs', 'dash_log')
    op.alter_column("api_service_log", "time", new_column_name="execution_time", existing_type=sa.Float(),
                    nullable=False)
    op.alter_column("api_service_log", "created_at", new_column_name="date_created", existing_type=sa.DateTime(),
                    nullable=False)
    op.create_table(
        'api_service',
        sa.Column('service_id', TINYINT(unsigned=True), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
    )
    op.create_table(
        'api_user',
        sa.Column('user_id', TINYINT(unsigned=True), primary_key=True),
        sa.Column('nickname', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('is_active', TINYINT(unsigned=True), nullable=False, default=1),
    )

    session.execute(delete(ApiServiceLog))
    op.alter_column("api_service_log", "service", new_column_name="service_id", existing_type=TINYINT(unsigned=True),
                    nullable=False)
    op.create_foreign_key(
        'fk_api_service_log_api_service',
        'api_service_log', 'api_service',
        ['service_id'], ['service_id'],
    )
    op.alter_column("api_service_log", "user", new_column_name="api_user_id", existing_type=TINYINT(unsigned=True),
                    nullable=True)
    op.create_foreign_key(
        'fk_api_service_log_api_user',
        'api_service_log', 'api_user',
        ['api_user_id'], ['user_id'],
    )
    session.execute(insert(ApiService, values={ApiService.name: "dynamic-frozen-group"}))
    session.execute(insert(ApiUser, values={ApiUser.nickname: "edusson", ApiUser.password: "+vju7VwmhNXz]9(."}))
    session.execute(insert(ApiUser, values={ApiUser.nickname: "test", ApiUser.password: "Q8UtsemJHZEJxOnE"}))
    session.commit()


def downgrade():
    op.rename_table('api_service_log', 'api_request_logs')
    op.rename_table('dash_log', 'logs')
    op.alter_column("api_request_logs", "execution_time", new_column_name="time", existing_type=sa.Float(),
                    nullable=False)
    op.alter_column("api_request_logs", "date_created", new_column_name="created_at", existing_type=sa.DateTime(),
                    nullable=False)

    op.drop_constraint(u'fk_api_service_log_api_service', 'api_request_logs', type_='foreignkey')
    op.alter_column("api_request_logs", "service_id", new_column_name="service", existing_type=sa.String(50),
                    nullable=False)

    op.drop_constraint(u'fk_api_service_log_api_user', 'api_request_logs', type_='foreignkey')
    op.alter_column("api_request_logs", "api_user_id", new_column_name="user", existing_type=sa.String(50),
                    nullable=False)

    op.drop_table('api_service')
    op.drop_table('api_user')
