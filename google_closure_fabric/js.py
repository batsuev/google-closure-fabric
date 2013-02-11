from base_builder import BaseBuilder

class JSBuilder(BaseBuilder):

    def __init__(self, project_path, advanced=True):
        BaseBuilder.__init__(self, project_path)
        if advanced:
            pass