from base_builder import BaseBuilder
from fabric.api import local
from pipes import quote
import os

class DepsBuilder(BaseBuilder):

    def set_output_file(self, path):
        self.__output_file = path

    def set_source(self, source):
        self.__source = source

    def build(self):
        BaseBuilder.build(self)
        if self.__output_file is None:
            raise Exception('output file not specified')

        base_js_path = os.path.join(self.closure_base_path, 'google-closure-library', 'closure', 'goog')
        deps_writer = os.path.join(self.closure_base_path, 'google-closure-library', 'closure', 'bin', 'build', 'depswriter.py')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --output_file=%s' % os.path.join(self.project_path, self.__output_file)
        if not(self.__source is None):
            folder = os.path.join(self.project_path, self.__source)
            base_js_relative_path = os.path.relpath(folder, base_js_path)
            args += " --root_with_prefix='%s %s'" % (quote(folder), quote(base_js_relative_path))

        local('python %s %s' % (deps_writer, args))
