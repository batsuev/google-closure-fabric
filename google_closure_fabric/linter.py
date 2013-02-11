__author__ = 'alex'
from base_builder import BaseBuilder
from fabric.api import local
import os

class Linter(BaseBuilder):

    __sources = []
    __excludes = []

    def __init__(self, project_path, strict = True):
        BaseBuilder.__init__(self, project_path)
        if strict:
            self.add_compiler_arg('--strict')

    def add_sources(self, sources):
        self.__sources.append(sources)

    def add_exclude(self, exclude):
        self.__excludes.append(exclude)

    def __get_excludes_arg(self):
        if len(self.__excludes) == 0: return ''
        return ' -x %s' % ','.join([os.path.join(self.project_path, ex) for ex in self.__excludes])

    def __get_sources_arg(self):
        if len(self.__sources) == 0:
            raise Exception('No sources specified')

        return ' -r %s' % ','.join([os.path.join(self.project_path, src) for src in self.__sources])

    def __get_args(self):
        args = self.get_compiler_args_str()
        args += self.__get_sources_arg()
        args += self.__get_excludes_arg()
        return args

    def autofix(self):
        BaseBuilder.build(self)

        local('fixjsstyle %s' % self.__get_args())

    def lint(self):
        BaseBuilder.build(self)

        local('gjslint %s' % self.__get_args())

