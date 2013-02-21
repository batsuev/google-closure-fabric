from base_builder import BaseBuilder
from fabric.api import local
from pipes import quote
import os

class DepsBuilder(BaseBuilder):

    def set_output_file(self, path):
        self.__output_file = path

    def set_source(self, source):
        self.__source = source

    def set_custom_path_prefix(self, path):
        self.__custom_path_prefix = path

    def build(self):
        BaseBuilder.build(self)
        if self.__output_file is None:
            raise Exception('output file not specified')

        deps_writer = os.path.join(self.closure_base_path, 'google-closure-library', 'closure', 'bin', 'build', 'depswriter.py')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --output_file=%s' % os.path.join(self.project_path, self.__output_file)
        if not(self.__source is None):
            folder = os.path.join(self.project_path, self.__source)
            args += " --root_with_prefix=\"%s %s\"" % (quote(folder), quote(self.__get_path_prefix()))

        local('python %s %s' % (deps_writer, args))

    def __get_path_prefix(self):
        if self.__custom_path_prefix is None:
            base_js_path = os.path.join(self.closure_base_path, 'google-closure-library', 'closure', 'goog')
            folder = os.path.join(self.project_path, self.__source)
            return os.path.relpath(folder, base_js_path)
        else:
            return self.__custom_path_prefix
