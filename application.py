import os.path

import engineio.async_gevent
import eventlet
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# eventlet.monkey_patch(thread=False)


import socketio
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


# https://code-live.ru/post/chat-with-tornado-backbone-and-websockets/

class EchoWebSocket(WebSocketHandler):
    def get(self):
        self.render('index.html')

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


# sio = socketio.AsyncServer(async_mode='tornado', message_queue='redis://172.17.0.2')
sio = socketio.AsyncServer(async_mode='tornado')
# socketio_app = SocketIO(app, message_queue='redis://{}'.format(app.config['REDIS_IP']))

async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        print('background_task')
        await sio.emit('my response', {'data': 'Server generated event'},
                       namespace='/test')


from threading import Thread

# thread = Thread(target=async
# lambda x: await
# background_task())
# thread.start()


@sio.on('my event', namespace='/test')
async def test_message(sid, message):
    print('test_message', sid, message)
    await sio.emit('my response', {'data': "sio.sleep 0"}, room=sid,
                   namespace='/test')

    # await engineio.async_gevent.sleep(5)
    sio.sleep(5)
    # await sio.sleep(2)
    print('test_message after sio.sleep', sid, message)

    await sio.emit('my response', {'data': 'sio.sleep  1'}, room=sid,
                   namespace='/test')
    sys.stdout.flush()
    sio.sleep(5)


    await sio.sleep(3)
    print('test_message after sio.sleep2 ', sid, message)

    await sio.emit('my response', {'data': 'sio.sleep 2'}, room=sid,
                   namespace='/test')
    sys.stdout.flush()
    await sio.sleep(4)
    print('test_message after sio.sleep 4 ', sid, message)

    await sio.emit('my response', {'data': 'sio.sleep 4'}, room=sid,
                   namespace='/test')

    # await background_task()


@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid, namespace='/test')


@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    await sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
                   namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                    difference=noun3)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', PoemPageHandler),
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
