__author__ = 'alex'
from base_builder import BaseBuilder
from fabric.api import local
import os

class Linter(BaseBuilder):

    def __init__(self, project_path, strict = True, ignore_80_symbols = False):
        BaseBuilder.__init__(self, project_path)
        self.__sources = []
        self.__excludes = []
        self.__ignore_80_symbols = ignore_80_symbols

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

        executable = self.__get_autofix_executable()

        local('%s %s' % (executable, self.__get_args()))

    def lint(self):
        BaseBuilder.build(self)

        executable = self.__get_linter_executable()

        local('%s %s' % (executable, self.__get_args()))

    def __get_linter_executable(self):
        if self.__ignore_80_symbols:
            return 'python %s' % os.path.join(os.path.dirname(__file__), 'gjslint_ext', 'linter.py')
        else:
            return 'gjslint'

    def __get_autofix_executable(self):
        if self.__ignore_80_symbols:
            return 'python %s' % os.path.join(os.path.dirname(__file__), 'gjslint_ext', 'autofix.py')
        else:
            return 'fixjsstyle'
