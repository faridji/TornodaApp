import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    dictionary = {'customers': ['Farid', 'Yousaf']}

    # this method is called at the start of each request
    def prepare(self):
        print("prepare method")

    def post(self):
        name = tornado.escape.json_decode(self.request.body)
        self.dictionary['customers'].append(name)
        self.render("customer.html", title="Customers", customers=self.dictionary['customers'])

    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        print(data)
        self.dictionary['customers'][data['index']] = data['name']
        self.render("customer.html", title="Customers", customers=self.dictionary['customers'])

    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        del self.dictionary['customers'][data['index']]
        self.render("customer.html", title="Customers", customers=self.dictionary['customers'])

    # This method is called at the end of each request;
    def on_finish(self):
        print("on_finish method")


class WebHandler(tornado.web.RequestHandler):
    dictionary = {'customers': ['Farid', 'Yousaf']}

    def prepare(self):
        print("prepare method")

    def get(self):
        self.render("customer.html", title="Customers", customers=self.dictionary['customers'])

    def on_finish(self):
        print("on_finish method")


class CustomerHandler(tornado.web.RequestHandler):
    dictionary = {'customers': ['Farid', 'Yousaf']}

    def prepare(self):
        print("prepare method")

    def get(self, customer_id):
        customer = self.dictionary['customers'][int(customer_id)]
        if customer is not None:
            self.render("customer.html", title="Customers", customers=customer)
        else:
            self.send_error('Please provide valid id', 400)

    def on_finish(self):
            print("on_finish method")




