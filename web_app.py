import tornado.ioloop
import tornado.web

from handler import MainHandler, WebHandler, CustomerHandler

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
        settings = {
            'debug': True,
            'compress_response': True,
            'template_path': 'templates/',
            'static_url_prefix': '/assets/',
            'autoreload': False,
            'xsrf_cookies': False,
        }

        super().__init__(handlers=[
            (r"/api/customers/([0-9]+)", CustomerHandler),
            (r"/api/customers", MainHandler),
            (r"/", WebHandler)], **settings)

    def start_server(self):
        self.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
        print("Server is listening on port", self.port)


