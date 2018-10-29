import json

import tornado.web
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

class BoardsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        boards = [
            {'name':'Board1', 'description': 'test 1', 'name_tag': 'tag', 'is_active': '1', 'date_created': '2018-10-10 10:10:10'},
            {'name':'Board2', 'description': 'test 2', 'name_tag': 'tag', 'is_active': '1', 'date_created': '2018-10-10 10:10:10'},
            {'name':'Board3', 'description': 'test 3', 'name_tag': 'tag', 'is_active': '1', 'date_created': '2018-10-10 10:10:10'},
            {'name':'Board4', 'description': 'test 4', 'name_tag': 'tag', 'is_active': '1', 'date_created': '2018-10-10 10:10:10'},
            {'name':'Board5', 'description': 'test 5', 'name_tag': 'tag', 'is_active': '1', 'date_created': '2018-10-10 10:10:10'},
            {'name':'Board6', 'description': 'test 6', 'name_tag': 'tag', 'is_active': '1', 'date_created': '2018-10-10 10:10:10'},
        ]
        self.write(json.dumps(boards))

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                    difference=noun3)
