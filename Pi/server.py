# import required tornado elements
import tornado.isloop
import tornado.web

# utility libraries
import os.path

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html')
    
class AdminHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('admin.html')
    
# Static file locations
settings = dict(
  template_path=os.path.join(os.path.dirname(__file__), "templates"),
  static_path=os.path.join(os.path.dirname(__file__), "static"),
  debug=True)
  
# r"/" is root address for localhost
application - tornado.web.Application((
  (r"/", MainHandler),
  (r"/", AdminHandler),
  ), **settings)
  
if __name__ == "__main__":
  print 'server running...'
  print 'press ctrl+c to close'
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
