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
        self.render('tank.html')

    def post(self, input):
        aquarium_id = input
        heater = self.get_argument('Heating', '')
        lighting = self.get_argument('Light', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')

        if heater == 'ON':
            #turn relay on for heating on that particular tank
            #self.write('switching relay ON')
            self.finish("switching relay ON")
        elif heater == 'OFF':
            #turn relay off for heating on that particular tank
            self.finish("switching relay OFF")
        else:
            #No action Required
            #self.write('parameter not defined for heating')
            x=1

        if lighting == '1':
            self.finish("toggle FRONT light")
        elif lighting == '2':
            self.finish("Toggle BACK light")
        elif lighting == '3':
            self.finish("Toggle TOP Light")
        else:
            #No action Required
            #self.write('parameter not defined for heating')
            x=2

        login_response = 'Min temp threshold: ' + mintemp_data + ', Max temp threshold: ' + maxtemp_data
        self.finish("Aquarium Number:" + aquarium_id + " " + login_response)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/aquarium(\d+)", TankHandler),
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
