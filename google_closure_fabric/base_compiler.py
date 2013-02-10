__author__ = 'alex'
from pipes import quote

class BaseCompiler:
    __compiler_path = None
    __compiler_args = []

    def set_compiler_path(self, path):
        self.__compiler_path = quote(path)

    def add_compiler_arg(self, name, value = None):
        self.__compiler_args.append(name)
        if value is not None:
            self.__compiler_args.append(value)

    def get_compiler_args_str(self):
        if self.__compiler_args.count() > 0:
            return ' '.join([quote(arg) for arg in self.__compiler_args])
        return ''

    def build(self):
        if self.__compiler_path is None:
            raise Exception('Compiler path is None')
