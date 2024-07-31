import json

class JSONSerializableFunction(dict):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool


class FunctionSet():
    def __iter__(self):
        return iter(self.functions)

    def __repr__(self):
        return repr(self.functions)

class Messages(list):

    def __repr__(self):
        return json.dumps(self, indent=2, ensure_ascii=False)