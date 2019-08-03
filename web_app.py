import tornado.ioloop
import tornado.web
# from tornado_sqlalchemy import make_session_factory

import os;
from handler import MainHandler, TemplateHandler


class WebApp(tornado.web.Application):
    port = 4000
    settings = {
        'debug': True,
        'compress_response': True,
        'template_path': 'templates/',
        'static_url_prefix': '/assets/',
        'autoreload': False,
        'xsrf_cookies': False,
    }

    def __init__(self):
        # factory = make_session_factory('db_url')

        settings = {
            'debug': True,
            'compress_response': True,
            'template_path': 'templates/',
            'static_url_prefix': '/assets/',
            'autoreload': False,
            'xsrf_cookies': False,
        }

        super().__init__(handlers=[
            (r"/api/compositions", MainHandler),
            (r"/api/templates", TemplateHandler)], **settings)

    def start_server(self):
        self.listen(self.port)
        print("Server is listening on port", self.port)
        tornado.ioloop.IOLoop.current().start()


