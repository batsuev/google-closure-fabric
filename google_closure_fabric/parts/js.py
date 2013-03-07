import sys
import os
from fabric.api import local, hide, settings
from ..base.base_builder import BaseObservableBuilder

class JSBuilder(BaseObservableBuilder):

    def __init__(self, project_path, advanced=True):
        BaseObservableBuilder.__init__(self, project_path)
        if advanced:
            self.add_compiler_arg('--compilation_level', 'ADVANCED_OPTIMIZATIONS')
            self.add_compiler_arg('--define', 'goog.DEBUG=false')

            self.add_compiler_arg('--jscomp_error', 'accessControls')
            self.add_compiler_arg('--jscomp_error', 'ambiguousFunctionDecl')
            # self.add_compiler_arg('--jscomp_error', 'cast')
            self.add_compiler_arg('--jscomp_error', 'checkRegExp')
            self.add_compiler_arg('--jscomp_error', 'checkTypes')
            self.add_compiler_arg('--jscomp_error', 'checkVars')
            self.add_compiler_arg('--jscomp_error', 'const')
            self.add_compiler_arg('--jscomp_error', 'constantProperty')
            self.add_compiler_arg('--jscomp_error', 'deprecated')
            self.add_compiler_arg('--jscomp_error', 'duplicateMessage')
            self.add_compiler_arg('--jscomp_error', 'es5Strict')
            self.add_compiler_arg('--jscomp_error', 'externsValidation')
            self.add_compiler_arg('--jscomp_error', 'fileoverviewTags')
            self.add_compiler_arg('--jscomp_error', 'globalThis')
            self.add_compiler_arg('--jscomp_error', 'internetExplorerChecks')
            self.add_compiler_arg('--jscomp_error', 'invalidCasts')
            self.add_compiler_arg('--jscomp_error', 'misplacedTypeAnnotation')
            self.add_compiler_arg('--jscomp_error', 'missingProperties')
            self.add_compiler_arg('--jscomp_error', 'nonStandardJsDocs')
            self.add_compiler_arg('--jscomp_error', 'suspiciousCode')
            self.add_compiler_arg('--jscomp_error', 'strictModuleDepCheck')
            self.add_compiler_arg('--jscomp_error', 'typeInvalidation')
            self.add_compiler_arg('--jscomp_error', 'undefinedNames')
            self.add_compiler_arg('--jscomp_error', 'undefinedVars')
            self.add_compiler_arg('--jscomp_error', 'unknownDefines')
            self.add_compiler_arg('--jscomp_error', 'uselessCode')
            self.add_compiler_arg('--jscomp_error', 'visibility')

            self.add_compiler_arg('--warning_level', 'VERBOSE')
            self.add_compiler_arg('--summary_detail_level', '3')

            self.add_compiler_arg('--generate_exports')

    def set_output_file(self, path):
        self.__output_file = path

    def set_sources_folder(self, path):
        self.__sources_folder = path

    def set_main_file(self, file):
        self.__main_file = file

    def get_watch_targets(self):
        return [self.__sources_folder]

    def watch_build(self):
        self.build(False)

    def build(self, fail_on_error=True):
        BaseObservableBuilder.build(self)

        if self.__output_file is None:
            raise Exception('No output file specified')

        if self.__sources_folder is None:
            raise Exception('No sources folder specified')

        if self.__main_file is None:
            raise Exception('No main file specified')

        print 'Building javascript... '

        sys.path.append(os.path.join(self.closure_base_path, 'google-closure-library', 'closure', 'bin'))
        import calcdeps

        js_out = os.path.join(self.project_path, self.__output_file)
        js_src = os.path.join(self.project_path, self.__sources_folder)
        closure_src = os.path.join(self.closure_base_path, 'google-closure-library', 'closure', 'goog')
        closure_compiler = os.path.join(self.closure_base_path, 'google-closure-compiler', 'compiler.jar')

        args = list(self.get_compiler_args())

        args.append('--js_output_file')
        args.append(js_out)

        args.append('--js')
        args.append('%s/deps.js' % closure_src)

        search_paths = calcdeps.ExpandDirectories([js_src, closure_src])

        sources = calcdeps.CalculateDependencies(search_paths, [os.path.join(js_src, self.__main_file)])
        for src in sources:
            args.append('--js')
            args.append(src)


        with hide('running'):
            with settings(warn_only=not fail_on_error):
                local('java -jar %s %s' % (closure_compiler, ' '.join(args)))