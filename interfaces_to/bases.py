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

import threading

class Messages(list):

    # accept verbose as a parameter in addition to the messages
    def __init__(self, *args, verbose=False, print_fn=None, listeners=[]):
        super().__init__(*args)
        self.verbose = verbose
        self.print_fn = print_fn
        if self.print_fn == None:
            self.print_fn = print
        self.listeners = listeners

        # if verbose and self:
        #     for message in self:
        #         self.print_fn(message)
        
        if listeners:
            self.condition = threading.Condition()
            threading.Thread(target=listeners[0], args=(self,), daemon=True).start()

    # override append to check if verbose is set
    def append(self, message):
        if self.verbose:
            self.print_fn(message)

        super().append(message)

        if hasattr(self, 'condition'):
            with self.condition:
                self.condition.notify()
    
    def block_if_empty(self):
        with self.condition:
            while not self:
                self.condition.wait()
    
    def clear_if_finished(self):
        if self and (self[-1]['role'] == 'assistant' and 'tool_calls' not in self[-1]):
            self.clear()

    def __repr__(self):
        return json.dumps(self, indent=2, ensure_ascii=False)