#Tornado elements
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

# utility libraries
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')

    def post(self):
        say_data = self.get_argument('say', '')
        to_data = self.get_argument('to', '')

        #login_response = {
        #    'say': say_data,
        #    'to': to_data,
        #    'msg': 'Data received;'
        #}
        login_response = 'say ' + say_data + ' to ' + to_data
        self.write(login_response)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
        self.write_message("connected")
 
    def on_message(self, message):
        print ('message received %s' % message)
        self.write_message('message received %s' % message)
 
    def on_close(self):
        print ('connection closed')
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/test", PostHandler),
            (r"/ws", WebSocketHandler)
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
