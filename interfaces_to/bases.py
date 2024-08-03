import json

class JSONSerializableFunction(dict):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool


class FunctionSet():
    def __init__(self, token=None, functions=None):
        self.token = token
        self.functions_map = self.create_functions_map()
        self.functions = self.instantiate_functions(functions)

    def create_functions_map(self):
        return {
            function.__name__: function._class
            for function in self.__class__.__dict__.values()
            if hasattr(function, "_callable")
        }

    def instantiate_functions(self, functions):
        if functions is None:
            functions = self.functions_map.keys()
        return [self.functions_map[function](self) for function in functions]


    def __iter__(self):
        return iter(self.functions)

    def __repr__(self):
        return repr(self.functions)

class Messages(list):

    def __repr__(self):
        return json.dumps(self, indent=2, ensure_ascii=False)