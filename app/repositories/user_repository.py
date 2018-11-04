from datetime import datetime

from passlib.handlers.sha2_crypt import sha256_crypt

from .board_repository import BoardRepository
from .repository import Repository
from edusson_ds_main.db.models import DashDashboardBoard, DashUser, DashUserBoardAccess


dashboard_id = 2


class UserRepository(Repository):
    def get(self, id):
        return self.session.query(DashUser).filter_by(user_id=id).first()

    def all(self):
        return self.session.query(DashUser).order_by(DashUser.user_id).all()

    def create(self, username, password, is_active, access_level_id, boards=None):
        user = DashUser(
            username=username,
            password=sha256_crypt.encrypt(password),
            is_active=is_active,
            access_level_id=access_level_id
        )

        if boards:
            self.attach_boards(user, boards)
            # attach board, not boards

        self.session.add(user)
        self.session.commit()

    def attach_boards(self, user, boards):
        for board_id in boards:
            board_access = DashUserBoardAccess(
                user=user,
                dashboard_id=dashboard_id,
                board_id=board_id
            )
            user.boards.append(board_access)

    def update(self, user_id):
        user = self.get(user_id)

        user_board_accesses = BoardRepository.get_user_board_accesses(user_id)

        exists_ids = []

        # try to use map and filter

        for board_access in user_board_accesses:
            exists_ids.append(board_access.board_id)

            if board_access.board_id not in boards:
                self.session.query(DashUserBoardAccess).filter_by(
                    user_id=id,
                    dashboard_id=dashboard_id,
                    board_id=board_access.board_id
                ).delete()

        not_exists_boards = filter(lambda x: x not in exists_ids, boards)
        # map(lambda x: )

        for board_id in boards:
            if board_id not in exists_ids:
                board_access = DashUserBoardAccess(
                    user=user,
                    dashboard_id=dashboard_id,
                    board_id=board_id
                )
                user.boards.append(board_access)

        user.username = username
        user.is_active = is_active

        if password:
            user.password = password

        if access_level_id:
            user.access_level_id = access_level_id

        self.session.commit()