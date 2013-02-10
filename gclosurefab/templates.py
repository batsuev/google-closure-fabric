__author__ = 'alex'
from fabric.api import local
from base_compiler import BaseCompiler
from pipes import quote

class GoogleClosureTemplatesBuilder(BaseCompiler):

    __output_path_format = None
    __inputs = []
    __deps = []

    def set_output_path_format(self, path):
        self.__output_path_format = path

    def add_source(self, path):
        self.__inputs.append(path)

    def add_dep(self, path):
        self.__deps.append(path)

    def build(self):
        super(GoogleClosureTemplatesBuilder, self).build()
        if self.__output_path_format is None:
            raise Exception('output_path_format required')
        if self.__inputs.count() == 0:
            raise Exception('No sources')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --output-path-format %s' % quote(self.__output_path_format)
        args += ' --srcs %s' % ','.join([quote(src) for src in self.__inputs])
        if self.__deps.count() > 0:
            args += ' --deps %s' % ','.join([quote(src) for src in self.__deps])
        local('java jar %s %s' % (self.__compiler_path, args))