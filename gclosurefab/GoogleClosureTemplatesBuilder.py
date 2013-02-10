__author__ = 'alex'
from fabric.api import local

class GoogleClosureTemplatesBuilder:

    __compiler_args = []
    __output_path_format = ''
    __inputs = []
    __deps = []

    def add_compiler_arg(self, name, value = None):
        self.__compiler_args.append(name)
        if value is not None:
            self.__compiler_args.append(value)

    def set_output_path_format(self, path):
        self.__output_path_format = path

    def add_source(self, path):
        self.__inputs.append(path)

    def add_dep(self, path):
        self.__deps.append(path)

    def build(self):
        pass