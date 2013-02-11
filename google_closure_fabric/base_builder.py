__author__ = 'alex'
from pipes import quote
import os

class BaseBuilder:
    __compiler_path = None
    __compiler_args = []

    closure_base_path = None
    project_path = None

    def __init__(self, project_path):
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
