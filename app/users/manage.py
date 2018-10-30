import json

from passlib.handlers.sha2_crypt import sha256_crypt

import application
import tornado.escape
from sqlalchemy.orm import sessionmaker
from tornado.websocket import WebSocketHandler
from edusson_ds_main.db.connections import DBConnectionsFacade
from edusson_ds_main.db.models import DashDashboardBoard, DashUser
from app.handlers import BasicHandler, to_dict

print('init my event')
@application.sio.on('my event', namespace='/test')
async def test_message(sid, message):
    print('test_message', sid, message)
    await application.sio.emit('my response', {'data': "sio.sleep 0"}, room=sid,
                   namespace='/test')


class UsersHandler(BasicHandler):
    def get(self):
        users = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashUser).all()
        users = [to_dict(DashUser, user) for user in users]
        self.write(json.dumps(users))

    def post(self):
        json_data = tornado.escape.json_decode(self.request.body)
        username = json_data.get('username')
        password = json_data.get('password')
        access_level_id = json_data.get('access_level_id')

        Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
        sess = Session()

        user = DashUser(
            username=username,
            password=sha256_crypt.encrypt(password),
            access_level_id=access_level_id
        )
        sess.add(user)
        sess.commit()


class UserHandler(BasicHandler):
    def get(self, id):
        id = int(id)
        user = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashUser).filter_by(
            user_id=id).first()

        if not user:
            return self.write(json.dumps({}))

        self.write(json.dumps(to_dict(DashUser, user)))

    def put(self, id):
        json_data = tornado.escape.json_decode(self.request.body)
        user_id = json_data.get('user_id', None)
        name = json_data.get('name')
        model_tag = json_data.get('model_tag')
        description = json_data.get('description')

        Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
        sess = Session()

        user = sess.query(DashUser).filter_by(
            user_id=id).first()

        user.name = name
        user.model_tag = model_tag
        user.description = description

        sess.commit()