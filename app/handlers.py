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

    def write_error(self, status_code, **kwargs):
        #http://nanvel.name/2014/12/handle-errors-in-tornado-application

        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.finish(json.dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                    'traceback': lines,
                }
            }))
        else:
            self.finish(json.dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                }
            }))







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
