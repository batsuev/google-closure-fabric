__author__ = 'alex'
from fabric.api import local
from base_builder import BaseBuilder
import os

class StylesheetsBuilder(BaseBuilder):

    __output_file = None
    __inputs = []

    def set_output_file(self, path):
        self.__output_file = path

    def add_stylesheet(self, stylesheet):
        self.__inputs.append(stylesheet)

    def build(self):
        BaseBuilder.build(self)

        if self.__output_file is None:
            raise Exception('output_file required')
        if len(self.__inputs) == 0:
            raise Exception('No sources')

        builder_path = os.path.join(self.closure_base_path, 'google-closure-stylesheets', 'closure-stylesheets.jar')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --output-file %s' % os.path.join(self.project_path, self.__output_file)
        args += ' '+','.join([os.path.join(self.project_path, src) for src in self.__inputs])

        local('java -jar %s %s' % (builder_path, args))