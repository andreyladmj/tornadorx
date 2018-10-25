import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


import socketio
from tornado.options import define, options

# print('init sio')
# mgr = socketio.AsyncRedisManager('redis://172.17.0.2')
# sio = socketio.AsyncServer(async_mode='tornado', client_manager=mgr)
sio = socketio.AsyncServer(async_mode='tornado')

from app.handlers import IndexHandler, EchoWebSocket


if __name__ == '__main__':
    define("port", default=8000, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/websocket', EchoWebSocket),
            (r"/socket.io/", socketio.get_tornado_handler(sio)),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static"},),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    # sio.attach(app)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
