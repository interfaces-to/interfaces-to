import json
import os

class JSONSerializableFunction(dict):
    token = None

    def __init__(self, tool):
        super().__init__()
        self.tool = tool


class FunctionSet():
    token_env_name = None

    def __init__(self, token=None, functions=None):
        self.token = token
        # try and load the token from the environment
        if token is None and self.token_env_name:
            try:
                self.token = os.environ[self.token_env_name]
            except KeyError:
                pass
         
        self.functions_map = self.create_functions_map()
        self.functions = self.instantiate_functions(functions)

    def create_functions_map(self):
        return {
            function.__name__: _inject_token(function._class, self.token)
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

def _inject_token(cls, token):
    cls.token = token
    return cls

class Messages(list):

    # accept verbose as a parameter in addition to the messages
    def __init__(self, messages, verbose=False, pretty_printer=None):
        super().__init__(messages)
        self.verbose = verbose

        if pretty_printer:
            self.print_fn = pretty_printer
        else:
            self.print_fn = print

        if verbose:
            for message in messages:
                self.print_fn(message)

    # override append to check if verbose is set
    def append(self, message):
        if self.verbose:
            self.print_fn(message)

        super().append(message)

    def __repr__(self):
        return json.dumps(self, indent=2, ensure_ascii=False)