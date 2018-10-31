import json

from passlib.handlers.sha2_crypt import sha256_crypt

import application
import tornado.escape
from sqlalchemy.orm import sessionmaker
from tornado.websocket import WebSocketHandler
from edusson_ds_main.db.connections import DBConnectionsFacade
from edusson_ds_main.db.models import DashDashboardBoard, DashUser, DashUserBoardAccess
from app.handlers import BasicHandler, to_dict, MyAppException
import tornado.web

# print('init my event')
# @application.sio.on('my event', namespace='/test')
# async def test_message(sid, message):
#     print('test_message', sid, message)
#     await application.sio.emit('my response', {'data': "sio.sleep 0"}, room=sid,
#                    namespace='/test')


dashboard_id = 1

class UsersHandler(BasicHandler):
    def get(self):
        users = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashUser).all()
        users = [to_dict(user) for user in users]
        self.write(json.dumps(users))

    def post(self):
        sess = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())()

        json_data = tornado.escape.json_decode(self.request.body)
        username = json_data.get('username')
        password = json_data.get('password')
        boards = json_data.get('boards', [])
        access_level_id = json_data.get('access_level_id')
        is_active = json_data.get('is_active')

        if not password:
            raise MyAppException(reason='password cannot be empty', status_code=400)

        if not username:
            raise MyAppException(reason='username cannot be empty', status_code=400)

        user = DashUser(
            username=username,
            password=sha256_crypt.encrypt(password),
            is_active=is_active,
            access_level_id=access_level_id
        )

        for board_id in boards:
            board_access = DashUserBoardAccess(
                user=user,
                dashboard_id=dashboard_id,
                board_id=board_id
            )
            user.boards.append(board_access)

        sess.add(user)
        sess.commit()


class UserHandler(BasicHandler):
    def get(self, id):
        id = int(id)
        # user = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashUser).outerjoin(DashUser.boards).filter_by(
        user = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashUser).filter_by(
            user_id=id).first()

        if not user:
            raise MyAppException(reason='User cannot be found', status_code=400)

        user = to_dict(user)
        user['boards'] = list(map(lambda x: x['board_id'], user['boards']))

        self.write(json.dumps(user))

    def put(self, id):
        json_data = tornado.escape.json_decode(self.request.body)
        username = json_data.get('username')
        password = json_data.get('password', None)
        boards = json_data.get('boards', [])
        access_level_id = json_data.get('access_level_id', None)

        sess = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())()

        user = sess.query(DashUser).filter_by(user_id=id).first()

        user_board_accesses = sess.query(DashUserBoardAccess).filter_by(user_id=id, dashboard_id=dashboard_id).all()

        exists_ids = []
        for board_access in user_board_accesses:
            exists_ids.append(board_access.board_id)

            if board_access.board_id not in boards:
                sess.delete(board_access)

        for board_id in boards:
            if board_id not in exists_ids:
                board_access = DashUserBoardAccess(
                    user=user,
                    dashboard_id=dashboard_id,
                    board_id=board_id
                )
                user.boards.append(board_access)

        user.username = username

        if password:
            user.password = password

        if access_level_id:
            user.access_level_id = access_level_id

        sess.commit()

    def delete(self, id):
        print('delete', id)
        user = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashUser).filter_by(
            user_id=id).first()
        Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
        sess = Session()
        sess.delete(user)
        sess.commit()
