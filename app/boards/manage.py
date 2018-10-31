import json

import tornado.escape
from sqlalchemy.orm import sessionmaker
from tornado.websocket import WebSocketHandler
from edusson_ds_main.db.connections import DBConnectionsFacade
from edusson_ds_main.db.models import DashDashboardBoard, DashUser

from app.handlers import BasicHandler, to_dict


class BoardHandler(BasicHandler):
    def get(self, id):
        id = int(id)
        board = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashDashboardBoard).filter_by(
            board_id=id).first()

        if not board:
            return self.write(json.dumps({}))

        self.write(json.dumps(to_dict(board)))

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

    def delete(self, id):
        print('delete', id)
        board = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashDashboardBoard).filter_by(
            board_id=id).first()
        Session = sessionmaker(bind=DBConnectionsFacade.get_edusson_ds())
        sess = Session()
        sess.delete(board)
        sess.commit()

class BoardsHandler(BasicHandler):
    def get(self):
        boards = DBConnectionsFacade.get_edusson_ds_orm_session().query(DashDashboardBoard).all()
        boards = [to_dict(board) for board in boards]
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