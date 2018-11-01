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
from app.boards.manage import BoardHandler, BoardsHandler
from app.users.manage import UsersHandler, UserHandler

sio = socketio.AsyncServer(async_mode='tornado')

from app.handlers import IndexHandler, EchoWebSocket

if __name__ == '__main__':

    from edusson_ds_main.db.connections import DBConnectionsFacade, DB_EDUSSON_DS
    DB_EDUSSON_DS.set_static_connection(pool_recycle=500, pool_size=10, max_overflow=0, engine='mysql+pymysql',
                                        host='159.69.44.90', db='edusson_tmp_boards', user='root', passwd='')

    define("port", default=8000, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/board/([^/]+)', BoardHandler),
            (r'/boards', BoardsHandler),
            (r'/users', UsersHandler),
            (r'/user/([^/]+)', UserHandler),
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
