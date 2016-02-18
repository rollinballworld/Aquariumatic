import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class TankHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.render('tank.html', test1="100 Degrees C", test2="14.0")

    def post(self, input):
        aquarium_id = input
        heater = self.get_argument('Heating', '')
        lighting = self.get_argument('Light', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')

        if heater == 'ON':
            #turn relay on for heating on that particular tank
            #self.write('switching relay ON')
            self.finish(json.dumps({"msg":"heater ON"}))
        elif heater == 'OFF':
            #turn relay off for heating on that particular tank
            self.finish(json.dumps({"msg":"heater OFF"}))
        else:
            #No action Required
            #self.write('parameter not defined for heating')
            x=1

        if lighting == '1':
            self.finish(json.dumps({"msg":"Toggle Front light"}))
        elif lighting == '2':
            self.finish(json.dumps({"msg":"Toggle Back light"}))
        elif lighting == '3':
            self.finish(json.dumps({"msg":"Toggle Top light"}))
        else:
            #No action Required
            #self.write('parameter not defined for heating')
            x=2

        login_response = 'Min temp threshold: ' + mintemp_data + ', Max temp threshold: ' + maxtemp_data
        self.finish(json.dumps({"msg": + aquarium_id + ": " + login_response}))


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        example_response = {}
        example_response['name'] = 'example'
        example_response['width'] = 1020

        self.write(json.dumps(example_response))


    def post(self):
        json_obj = json_decode(self.request.body)
        print('Post data received')

        for key in list(json_obj.keys()):
            print('key: %s , value: %s' % (key, json_obj[key]))

        # new dictionary
        response_to_send = {}
        response_to_send['newkey'] = json_obj['key1']

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/test", TestHandler),
            (r"/aquarium(\d+)", TankHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
