import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import time
import os, sys
from aquarium import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    
    def post (self):
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        
        if WebCommand == 'Pi':
            if WebValue == 'Shutdown':
                if sys.platform == 'win32':
                    os.system('shutdown /s')
                else:
                    os.system('shutdown -h now')
            elif WebValue == 'Reboot':
                if sys.platform == 'win32':
                    os.system('shutdown /r')
                else:
                    os.system('shutdown -r now')
            else:
                print('No matching Pi Command')
                return
        elif WebCommand == 'Arduino':
            if WebValue == 'Reset':
                slave = Aquarium(0)
                slave.ResetSlave()
            else:
                print('No matching Arduino Command')
                return
        else:
            print('Command not recognised')


class TankHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.render('tank.html')

    def post(self, input):
        aquarium_id = input
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')
        minph_data = self.get_argument('Minph', '')
        maxph_data = self.get_argument('Maxph', '')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        aquarium = Aquarium(aquarium_id)
        
        if WebCommand == 'Heating':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(WebCommand, WebValue)
            self.write(json.dumps({"msg":"heater set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'Light':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(WebCommand, WebValue)
            self.write(json.dumps({"msg":"lights set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'Pump':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(WebCommand, WebValue)
            self.write(json.dumps({"msg":"water pump set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'UpdateValues':
            slave_json = aquarium.CurrentStatus().rstrip("'")[1:]
            loaded_json = json.loads(slave_json)
            print(loaded_json)
            update_response = {}
            update_response['TankNo'] = aquarium_id
            update_response['msg'] = loaded_json["msg"]
            update_response['TempValue'] = loaded_json["Temp"] + " " + chr(176) + "C"
            update_response['pHValue'] = loaded_json["pH"]
            update_response['LightValue'] = loaded_json["Lights"]
            update_response['PumpValue'] = loaded_json["Pump"]
            self.write(json.dumps(update_response))
            return
        else:
            self.write('parameter not defined')
            


class AquariumaticHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.render('aquariumatic.html')

    def post(self, input):
        aquarium_id = input
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')
        minph_data = self.get_argument('Minph', '')
        maxph_data = self.get_argument('Maxph', '')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        aquarium = Aquarium(aquarium_id)
        
        if WebCommand == 'Heating':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(WebCommand, WebValue)
            self.write(json.dumps({"msg":"heater set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'Light':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(WebCommand, WebValue)
            self.write(json.dumps({"msg":"lights set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'Pump':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(WebCommand, WebValue)
            self.write(json.dumps({"msg":"water pump set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'UpdateValues':
            #print(WebCommand + ": " + WebValue)
            #aquarium.SendParameter(mintemp_data, maxtemp_data, minph_data, maxph_data)
            #aquarium.SendCommand(WebCommand, WebValue)
            update_response = {}
            update_response['TankNo'] = aquarium_id
            update_response['msg'] = 'Update requested'
            update_response['TempValue'] = aquarium.CurrentReading('Temp')
            update_response['pHValue'] = aquarium.CurrentReading('pH')
            update_response['LightValue'] = aquarium.CurrentReading('Light')
            update_response['PumpValue'] = aquarium.CurrentReading('Pump')
            self.write(json.dumps(update_response))
            return
        else:
            self.write('parameter not defined')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/aq(\d+)", AquariumaticHandler),
            (r"/tank(\d+)", TankHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
