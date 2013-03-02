__author__ = 'alex'
import os
import tempfile
from fabric.api import local
from ..base.base_builder import BaseObservableBuilder

class TemplatesBuilder(BaseObservableBuilder):

    def __init__(self, project_path, use_goog=True):
        self.__inputs = []
        self.__deps = []

        BaseObservableBuilder.__init__(self, project_path)
        if use_goog:
            self.add_compiler_arg('--shouldProvideRequireSoyNamespaces')
            self.add_compiler_arg('--shouldGenerateJsdoc')

    def set_output_path_format(self, path):
        self.__output_path_format = path

    def add_template(self, path):
        self.__inputs.append(path)

    def add_dep(self, path):
        self.__deps.append(path)

    def get_watch_targets(self):
        return self.__inputs + self.__deps

    def build(self):
        BaseObservableBuilder.build(self)
        if self.__output_path_format is None:
            raise Exception('output_path_format required')
        if len(self.__inputs) == 0:
            raise Exception('No sources')

        local('java -jar %s %s' % (self.__get_builder_path(), self.__get_args(output_path=os.path.join(self.project_path, self.__output_path_format))))

    def __get_args(self, output_path):
        args = ''
        args += self.get_compiler_args_str()

        args += ' --outputPathFormat %s' % output_path
        args += ' --srcs %s' % ','.join([os.path.join(self.project_path, src) for src in self.__inputs])
        if len(self.__deps) > 0:
            args += ' --deps %s' % ','.join([os.path.join(self.project_path, src) for src in self.__deps])
        return args

    def __get_builder_path(self):
        return os.path.join(self.closure_base_path, 'google-closure-templates', 'SoyToJsSrcCompiler.jar')

    def get_template(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        local('java -jar %s %s' % (self.__get_builder_path(),
                                   self.__get_args(output_path=f.name)))
        res = f.read()
        f.close()
        os.unlink(f.name)
        return res
