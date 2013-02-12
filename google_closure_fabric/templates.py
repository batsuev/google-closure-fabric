__author__ = 'alex'
from fabric.api import local
from base_builder import BaseBuilder
import os

class TemplatesBuilder(BaseBuilder):

    def __init__(self, project_path, use_goog=False):
        self.__inputs = []
        self.__deps = []

        BaseBuilder.__init__(self, project_path)
        if use_goog:
            self.add_compiler_arg('--shouldProvideRequireSoyNamespaces')
            self.add_compiler_arg('--shouldGenerateJsdoc')

    def set_output_path_format(self, path):
        self.__output_path_format = path

    def add_template(self, path):
        self.__inputs.append(path)

    def add_dep(self, path):
        self.__deps.append(path)

    def build(self):
        BaseBuilder.build(self)
        if self.__output_path_format is None:
            raise Exception('output_path_format required')
        if len(self.__inputs) == 0:
            raise Exception('No sources')

        builder_path = os.path.join(self.closure_base_path, 'google-closure-templates', 'SoyToJsSrcCompiler.jar')

        args = ''
        args += self.get_compiler_args_str()
        args += ' --outputPathFormat %s' % os.path.join(self.project_path, self.__output_path_format)
        args += ' --srcs %s' % ','.join([os.path.join(self.project_path, src) for src in self.__inputs])
        if len(self.__deps) > 0:
            args += ' --deps %s' % ','.join([os.path.join(self.project_path, src) for src in self.__deps])
        local('java -jar %s %s' % (builder_path, args))