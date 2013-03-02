import bootstrap, os
from SocketServer import TCPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class CustomServer(TCPServer):

    def __init__(self, project_path, server_address, RequestHandlerClass, deps_builder = None):
        self.project_path = project_path
        self.deps_builder = deps_builder
        TCPServer.__init__(self, server_address, RequestHandlerClass)


class RequestHandler(SimpleHTTPRequestHandler):

    def __get_google_closure_file(self):
        path = os.path.relpath(bootstrap.get_paths(self.server.project_path), self.server.project_path)
        path = os.path.join(path, 'google-closure-library', 'closure')
        self.path = path + self.path
        SimpleHTTPRequestHandler.do_GET(self)

    def __get_deps(self):
        deps_content = self.server.deps_builder.get_deps()

        self.send_response(200)
        self.send_header("Content-type", 'text/javascript')
        self.end_headers()

        self.wfile.write(deps_content)

    def do_GET(self):
        if self.path.startswith('/goog/'):
            self.__get_google_closure_file()
        elif self.path == '/deps' and not (self.server.deps_builder is None):
            self.__get_deps()
        else:
            SimpleHTTPRequestHandler.do_GET(self)

def serve(project_path, port = 8000, deps_builder = None, stylesheets_builder = None):
    httpd = CustomServer(project_path, ("", port), RequestHandler, deps_builder)
    print 'Server started: http://127.0.0.1:%s/' % port

    observer = None
    if stylesheets_builder is not None:
        observer = stylesheets_builder.watch()

    httpd.serve_forever()

    if stylesheets_builder is not None:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    serve('/Users/alex/Work/livemindmaps/frontend')