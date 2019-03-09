import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    customers = []

    # this method is called at the start of each request
    def prepare(self):
        print("prepare method")

    def get(self):
        self.render("customer.html", title="Customers", customers=self.customers)

    def post(self):
        name = tornado.escape.json_decode(self.request.body)
        self.customers.append(name)
        self.render("customer.html", title="Customers", customers=self.customers)

    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        self.customers[data['index']] = data['name']
        self.render("customer.html", title="Customers", customers=self.customers)

    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        del self.customers[data['index']]
        self.render("customer.html", title="Customers", customers=self.customers)

    # This method is called at the end of each request;
    def on_finish(self):
        print("on_finish method")


class CustomerHandler(tornado.web.RequestHandler):
    customers = []

    def prepare(self):
        print("prepare method")

    def get(self, customer_id):
        customer = self.customers
        if customer is not None:
            self.render("customer.html", title="Customers", customers=customer)
        else:
            self.send_error('Please provide valid id', 400)

    def on_finish(self):
            print("on_finish method")


class ProductHandler(tornado.web.RequestHandler):
    products = []

    # this method is called at the start of each request
    def prepare(self):
        print("prepare method")

    def get(self):
        self.render("products.html", title="Products", products=self.products)

    def post(self):
        name = tornado.escape.json_decode(self.request.body)
        self.products.append(name)
        self.render("products.html", title="Products", products=self.products)

    def put(self):
        data = tornado.escape.json_decode(self.request.body)
        self.products[data['index']] = data['name']
        self.render("products.html", title="Products", products=self.products)

    def delete(self):
        data = tornado.escape.json_decode(self.request.body)
        del self.products[data['index']]
        self.render("products.html", title="Products", products=self.products)

    # This method is called at the end of each request;
    def on_finish(self):
        print("on_finish method")



