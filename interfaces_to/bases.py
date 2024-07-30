class JSONSerializableFunction(dict):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool


class FunctionSet():
    def __iter__(self):
        return iter(self.functions)

    def __repr__(self):
        return repr(self.functions)
