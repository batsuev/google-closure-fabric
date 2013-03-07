from pipes import quote
import os, time, glob, hashlib
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

    def build(self, fail_on_error=True):
        pass


class ChangeEventHandler(FileSystemEventHandler):

    def __init__(self, builder):
        self.__builder = builder
        FileSystemEventHandler.__init__(self)

    def on_any_event(self, event):
        self.__builder.build_changes()


class BaseObservableBuilder(BaseBuilder):

    __built = False # will be implemented a bit later
    __hashes = {}

    def __has_changes(self):
        if not self.__built:
            return True
        new_hashes = self.__get_hashes()
        if len(set(self.__hashes.keys()) - set(new_hashes.keys())) > 0:
            return True

        for path in new_hashes.keys():
            if self.__hashes[path] != new_hashes[path]:
                return True

        return False

    def __hash(self, path):
        f = open(path, 'rb')
        step = 65536
        buf = f.read(step)
        hasher = hashlib.sha256()
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(step)
        return hasher.digest()

    def __get_hashes(self):
        res = {}
        for f in self.get_watch_targets():
            if not f.startswith(self.project_path):
                f = os.path.join(self.project_path, f)
            paths = glob.glob(f)
            for path in paths:
                res[path] = self.__hash(path)
        return res

    def build_changes(self):
        if self.__has_changes():
            self.build(fail_on_error=False)

    def build_complete(self):
        self.__built = True
        self.__hashes = self.__get_hashes()

    def get_watch_targets(self):
        raise Exception('Not implemented')

    def watch(self):
        self.build(fail_on_error=False)
        event_handler = ChangeEventHandler(self)

        folders = []
        for input in self.get_watch_targets():
            folder = os.path.dirname(os.path.join(self.project_path, input))
            if not folder in folders:
                folders.append(folder)

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
