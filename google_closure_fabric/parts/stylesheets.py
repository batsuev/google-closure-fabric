__author__ = 'alex'
import os
from fabric.api import local, hide, settings
from ..base.base_builder import BaseObservableBuilder

class StylesheetsBuilder(BaseObservableBuilder):

    def __init__(self, project_path):
        self.__inputs = []
        BaseObservableBuilder.__init__(self, project_path)

    def set_output_file(self, path):
        self.__output_file = path

    def add_stylesheet(self, stylesheet):
        self.__inputs.append(stylesheet)

    def get_watch_targets(self):
        return self.__inputs

    def build(self, fail_on_error=True):
        BaseObservableBuilder.build(self)

        if self.__output_file is None:
            raise Exception('output_file required')
        if len(self.__inputs) == 0:
            raise Exception('No sources')

        print 'Building stylesheets... '

        builder_path = os.path.join(self.closure_base_path, 'google-closure-stylesheets', 'closure-stylesheets.jar')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --output-file %s' % os.path.join(self.project_path, self.__output_file)
        args += ' '+','.join([os.path.join(self.project_path, src) for src in self.__inputs])

        with hide('running'):
            with settings(warn_only=not fail_on_error):
                local('java -jar %s %s' % (builder_path, args))

        self.build_complete()
