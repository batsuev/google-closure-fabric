__author__ = 'alex'
from fabric.api import local
from base_builder import BaseBuilder
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import os, time

class StylesheetsInputChangeEventHandler(FileSystemEventHandler):

    def __init__(self, builder):
        self.__builder = builder
        super(StylesheetsInputChangeEventHandler, self).__init__()

    def on_any_event(self, event):
        self.__builder.build()

class StylesheetsBuilder(BaseBuilder):

    def __init__(self, project_path):
        self.__inputs = []
        BaseBuilder.__init__(self, project_path)

    def set_output_file(self, path):
        self.__output_file = path

    def add_stylesheet(self, stylesheet):
        self.__inputs.append(stylesheet)

    def watch(self):
        event_handler = StylesheetsInputChangeEventHandler(self)

        folders = []
        for input in self.__inputs:
            folder = os.path.dirname(os.path.join(self.project_path, input))
            if not folder in folders:
                folders.append(folder)

        print 'Start monitoring inputs in %s' % folders

        observer = Observer()
        for input in folders:
            observer.schedule(event_handler, input, recursive=True)
        observer.start()

        return observer

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