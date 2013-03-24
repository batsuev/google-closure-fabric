import bootstrap, os
from SocketServer import TCPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class CustomServer(TCPServer):
    def __init__(self, project_path, server_address, RequestHandlerClass, deps_builder=None, js_builder=None,html_folder='.'):
        self.html_folder = html_folder
        self.project_path = project_path
        self.deps_builder = deps_builder
        self.js_builder = js_builder
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
        elif self.server.js_builder is not None and self.path == ('/'+self.server.js_builder.get_output_file()):
            self.server.js_builder.build_changes()
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            if os.path.exists(self.server.project_path + '/' + self.server.html_folder + '/' + self.path):
                self.path = self.server.html_folder + '/' + self.path
            SimpleHTTPRequestHandler.do_GET(self)


def serve(project_path, port=8000, html_folder='.', deps_builder=None, stylesheets_builder=None, templates_builder=None,
          js_builder=None):
    httpd = CustomServer(project_path, ("", port), RequestHandler, deps_builder, js_builder, html_folder)

    stylesheets_observer = None
    templates_observer = None

    if stylesheets_builder is not None:
        stylesheets_observer = stylesheets_builder.watch()

    if templates_builder is not None:
        templates_observer = templates_builder.watch()

    print 'Server started: http://127.0.0.1:%s/' % port
    print 'Start monitoring for changes'
    httpd.serve_forever()

    if stylesheets_observer is not None:
        stylesheets_observer.stop()
        stylesheets_observer.join()

    if templates_observer is not None:
        templates_observer.stop()
        templates_observer.join()