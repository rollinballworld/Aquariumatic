import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

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
        UpdateRequest = self.get_argument('UpdateValues', '')

        if heater == 'ON':
            #turn relay on for heating on that particular tank
            #self.write('switching relay ON')
            self.write(json.dumps({"msg":"heater ON"}))
            return
        elif heater == 'OFF':
            #turn relay off for heating on that particular tank
            self.write(json.dumps({"msg":"heater OFF"}))
            return
        else:
            #No action Required
            #self.write('parameter not defined for heating')
            x=1

        if lighting == '1':
            self.write(json.dumps({"msg":"Toggle Front light"}))
            return
        elif lighting == '2':
            self.write(json.dumps({"msg":"Toggle Back light"}))
            return
        elif lighting == '3':
            self.write(json.dumps({"msg":"Toggle Top light"}))
            return
        else:
            #No action Required
            #self.write('parameter not defined for heating')
            x=2

        update_response = {}
        update_response['TankNo'] = aquarium_id
        update_response['TempValue'] = '50 Degrees C'
        update_response['pHValue'] = '7.0'

        #login_response = 'Min temp threshold: ' + mintemp_data + ', Max temp threshold: ' + maxtemp_data
        #self.write(json.dumps({"msg": aquarium_id + ": " + login_response}))
        self.write(json.dumps(update_response))


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
        self.write(json.dumps(response_to_send))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/test", TestHandler),
            (r"/aquarium(\d+)", TankHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            js_path=os.path.join(template_path, "js"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
