from datetime import datetime

from .repository import Repository
from edusson_ds_main.db.models import DashDashboardBoard, DashUser, DashUserBoardAccess


dashboard_id = 2

class BoardRepository(Repository):
    def get(self, id):
        return self.session.query(DashDashboardBoard).filter_by(board_id=id).first()

    def create(self, name, model_tag, description):
        board = DashDashboardBoard(
            name=name,
            model_tag=model_tag,
            description=description,
            date_created=datetime.utcnow(),
        )

        self.session.add(board)
        self.session.commit()

    def get_user_board_accesses(self):
        return self.session.query(DashUserBoardAccess).filter_by(user_id=id, dashboard_id=dashboard_id).all()