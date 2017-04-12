import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import json
import time
import os, sys
#from aquariumUSB import *
from aquariumv3 import *
#from lcd import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        #lcd_string("Index Requested",LCD_LINE_1)
    
    def post (self):
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        
        if WebCommand == 'Pi':
            if WebValue == 'Shutdown':
                if sys.platform == 'win32':
                    os.system('shutdown /s')
                else:
                    #lcd_string("Shutting down...",LCD_LINE_2)
                    os.system('shutdown -h now')
            elif WebValue == 'Reboot':
                if sys.platform == 'win32':
                    os.system('shutdown /r')
                else:
                    #lcd_string("Rebooting...",LCD_LINE_2)
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
            aquarium.SendCommand(aquarium_id, WebCommand, WebValue)
            self.write(json.dumps({"msg":"heater set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'Light':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(aquarium_id, WebCommand, WebValue)
            self.write(json.dumps({"msg":"lights set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'Pump':
            #print(WebCommand + ": " + WebValue)
            aquarium.SendCommand(aquarium_id, WebCommand, WebValue)
            self.write(json.dumps({"msg":"water pump set to " + WebValue}, default=lambda x: None))
            return
        elif WebCommand == 'UpdateValues':
            slave_json = aquarium.CurrentStatus(aquarium_id).rstrip("'")[1:]
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
            

class SlaveSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, input):
        aquarium_id = input
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


#def UpdateIPs():
    #lcd_string("LAN: " + get_ip_address('eth0'),LCD_LINE_3)
    #lcd_string("IP_" + get_ip_address('wlan0'),LCD_LINE_2) 

if __name__ == "__main__":
    if sys.platform == 'win32':
        x=1
    else:
        #lcd_init()
        #lcd_string("Aquariumatic V3 ",LCD_LINE_1)
        #lcd_string("IP_" + get_ip_address('wlan0'),LCD_LINE_2)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/ss(\d+)", SlaveSocket),
            (r"/tank(\d+)", TankHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    main_loop = tornado.ioloop.IOLoop.instance()
    # Schedule event (5 seconds from now)
    #main_loop.call_later(5, UpdateIPs)
    # Start main loop
    main_loop.start()
