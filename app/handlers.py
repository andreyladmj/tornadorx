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


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                    difference=noun3)
