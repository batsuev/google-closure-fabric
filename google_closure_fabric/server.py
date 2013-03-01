import bootstrap, os
from SocketServer import TCPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class CustomServer(TCPServer):

    def __init__(self, project_path, server_address, RequestHandlerClass):
        self.project_path = project_path
        TCPServer.__init__(self, server_address, RequestHandlerClass)


class RequestHandler(SimpleHTTPRequestHandler):

    def __get_google_closure_file(self):
        path = os.path.relpath(bootstrap.get_paths(self.server.project_path), self.server.project_path)
        path = os.path.join(path, 'google-closure-library', 'closure')
        self.path = path + self.path
        SimpleHTTPRequestHandler.do_GET(self)

    def do_GET(self):
        if self.path.startswith('/goog/'):
            self.__get_google_closure_file()
        else:
            SimpleHTTPRequestHandler.do_GET(self)

def serve(project_path, port = 8000):
    print 'project path %s' % project_path
    httpd = CustomServer(project_path, ("", port), RequestHandler)
    print 'Server started: http://127.0.0.1:%s/' % port
    httpd.serve_forever()

if __name__ == '__main__':
    serve('/Users/alex/Work/livemindmaps/frontend')