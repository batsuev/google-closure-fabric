from pipes import quote
import os, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BaseBuilder:

    def __init__(self, project_path):
        self.__compiler_args = []
        self.project_path = project_path
        self.__init_closure_path()

    def __init_closure_path(self):
        closure_paths_file = os.path.join(self.project_path, '.closure_paths')
        if not os.path.exists(closure_paths_file):
            raise Exception('Closure paths file not found. Please call bootstrap() before using builders')
        closure_paths = open(closure_paths_file, 'r').read()
        closure_paths = os.path.join(self.project_path, closure_paths)
        if not os.path.exists(closure_paths):
            raise Exception('Closure library not found. Please call bootstrap() before using builders')
        self.closure_base_path = closure_paths

    def set_compiler_path(self, path):
        self.__compiler_path = quote(path)

    def add_compiler_arg(self, name, value = None):
        self.__compiler_args.append(name)
        if value is not None:
            self.__compiler_args.append(value)

    def get_compiler_args_str(self):
        if len(self.__compiler_args) > 0:
            return ' '.join([quote(arg) for arg in self.__compiler_args])
        return ''

    def get_compiler_args(self):
        return self.__compiler_args

    def build(self):
        pass


class ChangeEventHandler(FileSystemEventHandler):

    def __init__(self, builder):
        self.__builder = builder
        FileSystemEventHandler.__init__(self)

    def on_any_event(self, event):
        self.__builder.build()


class BaseObservableBuilder(BaseBuilder):

    def get_watch_targets(self):
        raise Exception('Not implemented')

    def watch(self):
        self.build()
        event_handler = ChangeEventHandler(self)

        folders = []
        for input in self.get_watch_targets():
            folder = os.path.dirname(os.path.join(self.project_path, input))
            if not folder in folders:
                folders.append(folder)

        print 'Start monitoring inputs in %s' % folders

        observer = Observer()
        for input in folders:
            observer.schedule(event_handler, input, recursive=True)
        observer.start()

        return observer

    def watch_forever(self):
        observer = self.watch()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
