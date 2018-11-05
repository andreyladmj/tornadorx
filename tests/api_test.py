import tornado
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase, AsyncHTTPTestCase
from tornado.web import Application
from app.boards.manage import BoardHandler, BoardsHandler
from app.users.manage import UsersHandler, UserHandler
from app.handlers import IndexHandler, EchoWebSocket


class MyTestCase(AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        response = yield client.fetch("http://www.tornadoweb.org")
        # Test contents of response
        self.assertIn("FriendFeed", response.body)

class MyHTTPTest(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            (r'/', IndexHandler),
            (r'/api/v1/board/([^/]+)', BoardHandler),
            (r'/api/v1/boards', BoardsHandler),
            (r'/api/v1/users', UsersHandler),
            (r'/api/v1/user/([^/]+)', UserHandler),
            (r'/api/v1/websocket', EchoWebSocket),
        ])

    def test_homepage(self):
        # The following two lines are equivalent to
        #   response = self.fetch('/')
        # but are shown in full here to demonstrate explicit use
        # of self.stop and self.wait.
        self.http_client.fetch(self.get_url('/api/v1/user/10'), self.stop)
        response = self.wait()
        print(dir(response))
        print(response.code)
        print(response.body)
        print(response.text)
        # test contents of response