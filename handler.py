import tornado.web
import json
import db


class MainHandler(tornado.web.RequestHandler):
    compositions = []

    # this method is called at the start of each request
    def prepare(self):
        print("prepare method")

    def get(self):
        data = db.makeJSON()
        return self.write(json.dumps(data))

    def post(self):
        data = json.loads(self.request.body)
        self.compositions.append(data['name'])
        return self.write(json.dumps(self.compositions))

    def put(self):
        data = json.loads(self.request.body)
        self.compositions[data['index']] = data['name']

    def delete(self):
        data = json.loads(self.request.body)
        del self.compositions[data['index']]

    # This method is called at the end of each request;
    def on_finish(self):
        print("on_finish method")


