__author__ = 'alex'
from pipes import quote
from fabric.api import local

from base_compiler import BaseCompiler

class GoogleClosureStylesheetsBuilder(BaseCompiler):

    __output_file = None
    __inputs = []

    def set_output_file(self, path):
        self.__output_file = path

    def add_stylesheet(self, stylesheet):
        self.__inputs.append(stylesheet)

    def build(self):
        super(GoogleClosureStylesheetsBuilder, self).build()
        if self.__output_file is None:
            raise Exception('output_file required')
        if self.__inputs.count() == 0:
            raise Exception('No sources')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --output-file %s' % quote(self.__output_file)
        args += ','.join([quote(src) for src in self.__inputs])

        local('java jar %s %s' % (self.__compiler_path, args))