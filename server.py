import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import aquarium

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
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        aquarium = Aquarium(aquarium_id)
        
        if WebCommand == 'Heating':
            print(WebCommand + ": " + WebValue)
            aquarium.SendCommand('test','')
            self.write(json.dumps({"msg":"heater set to " + WebValue}))
            return
        elif WebCommand == 'Light':
            print(WebCommand + ": " + WebValue)
            aquarium.SendCommand('test','')
            self.write(json.dumps({"msg":"lights set to " + WebValue}))
            return
        elif WebCommand == 'Pump':
            print(WebCommand + ": " + WebValue)
            aquarium.SendCommand('test','')
            self.write(json.dumps({"msg":"water pump set to " + WebValue}))
            return
        elif WebCommand == 'UpdateValues':
            print(WebCommand + ": " + WebValue)
            update_response = {}
            update_response['TankNo'] = aquarium_id
            update_response['msg'] = 'Update requested'
            update_response['TempValue'] = '50 Degrees C'
            update_response['pHValue'] = '7.0'
            self.write(json.dumps(update_response))
            return
        else:
            self.write('parameter not defined')
            


class TestHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.render('aquariumatic.html')

    def post(self, input):
        aquarium_id = input
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        if WebCommand == 'WaterChange':
            print(WebCommand + ": " + WebValue)
            self.write(json.dumps({"msg":"WaterChange Triggered."}))
            return
        elif WebCommand == 'Light':
            print(WebCommand + ": " + WebValue)
            self.write(json.dumps({"msg":"Light toggled"}))
            return
        elif WebCommand == 'Feed':
            print(WebCommand + ": " + WebValue)
            self.write(json.dumps({"msg":"Feeder triggered"}))
            return        
        elif WebCommand == 'UpdateValues':
            print(WebCommand + ": " + WebValue)
            update_response = {}
            update_response['TankNo'] = aquarium_id
            update_response['msg'] = 'Update requested'
            update_response['TempValue'] = '50 Degrees C'
            update_response['LightValue'] = 'ON'
            update_response['pHValue'] = '7.0'
            self.write(json.dumps(update_response))
            return
        else:
            self.write('parameter not defined')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/test(\d+)", TestHandler),
            (r"/aquarium(\d+)", TankHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
