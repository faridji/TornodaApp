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
        self.insertComposition(data)
        return self.write("Composition Added.")

    def put(self):
        data = json.loads(self.request.body)
        self.compositions[data['index']] = data['name']

    def delete(self):
        data = json.loads(self.request.body)
        del self.compositions[data['index']]

    # This method is called at the end of each request;
    def on_finish(self):
        print("on_finish method")

    def insertComposition(self, data):
        report_id = self.saveReportType(data['name'], data['type'], data['desc'])
        if report_id is not None:
            self.iterateJsonLocal(data['json_data'], {}, report_id)

    def saveReportType(self, name, type, desc):
        report_id = db.saveReportType(name, type, desc)
        return report_id

    def iterateJsonLocal(self,data, parent, report_id):
        self.writeToComposition(data, parent, report_id)
        for obj in data['children']:
            self.iterateJsonLocal(obj, data, report_id)

    def writeToComposition(self, command, parent, report_id):
        data = {}

        data['Type'] = command['objectType']
        data['Frame'] = command['frame']
        data['Name'] = command['object_id']
        data['Styles'] = command['backColor']
        data['Image_url'] = command.get('url', None)
        data['Label_text'] = command.get('text', None)
        data['Font_size'] = command.get('fontSize', None)
        data['Creator'] = 'Farid'
        data['type_id'] = report_id

        id = db.addToComposition(data)
        command['oid'] = id  # Save parent Id for future use

        parent_oid = parent.get('oid', None)  # get parent id of current item
        db.addToCompositionItem(id, parent_oid)



class TemplateHandler(tornado.web.RequestHandler):
    def prepare(self):
        print("prepare method")

    def get(self):
        data = db.loadTemplates()
        return self.write(json.dumps(data))

    def post(self):
        data = json.loads(self.request.body)
        db.addToTemplates(data['name'], data['type'], data['json_data'])

    # This method is called at the end of each request;
    def on_finish(self):
        print("on_finish method")
