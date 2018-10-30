import json

import tornado.web
import tornado.escape
from edusson_ds_main.db.connections import DBConnectionsFacade
from edusson_ds_main.db.models import DashDashboardBoard, DashUser
from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy.orm import sessionmaker
from tornado.websocket import WebSocketHandler


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class EchoWebSocket(WebSocketHandler):
    def get(self):
        self.render('index.html')

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


class BasicHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE')
        self.set_header("Content-type", "application/json")

    def options(self, *args, **kwargs):
        pass


class BoardHandler(BasicHandler):
    def get(self, id):
        id = int(id)
        board = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashDashboardBoard).filter_by(
            board_id=id).first()

        if not board:
            return self.write(json.dumps({}))

        self.write(json.dumps(to_dict(DashDashboardBoard, board)))

    def put(self, id):
        json_data = tornado.escape.json_decode(self.request.body)
        board_id = json_data.get('board_id', None)
        name = json_data.get('name')
        model_tag = json_data.get('model_tag')
        description = json_data.get('description')

        Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
        sess = Session()

        board = sess.query(DashDashboardBoard).filter_by(
            board_id=id).first()

        board.name = name
        board.model_tag = model_tag
        board.description = description

        sess.commit()

class BoardsHandler(BasicHandler):
    def get(self):
        boards = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashDashboardBoard).all()
        boards = [to_dict(DashDashboardBoard, board) for board in boards]
        self.write(json.dumps(boards))

    def post(self):
        json_data = tornado.escape.json_decode(self.request.body)
        board_id = json_data.get('board_id', None)
        name = json_data.get('name')
        model_tag = json_data.get('model_tag')
        description = json_data.get('description')

        Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
        sess = Session()

        log = DashDashboardBoard(
            name=name,
            model_tag=model_tag,
            description=description
        )
        sess.add(log)
        sess.commit()

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


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                    difference=noun3)


def to_dict(cls, obj):
    d = {}
    for i in cls.__dict__:
        if not i.startswith('_'):
            d[i] = getattr(obj, i)

    return d
