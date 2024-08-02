from ..bases import FunctionSet, JSONSerializableFunction
import time

class Self(FunctionSet):

    class Wait(JSONSerializableFunction):

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "wait",
                "description": "Wait for a specified amount of time. Useful if you want to call another tool in the near future and need to wait for a response. Avoid waiting more than 30 seconds at a time and instead try the tool call before waiting again if necessary.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "seconds": {
                            "type": "integer",
                            "description": "The number of seconds to wait",
                        },
                    },
                    "required": ["seconds"],
                },
            }

        def wait(self, seconds):
            
            time.sleep(seconds)

            return f"Waiting for {seconds} seconds"

    def __init__(self, token=None, functions=None):
        self.token = token

        # create a manual mapping of function names to classes
        self.functions_map = {
            'wait': self.Wait
        }

        if functions is None:
            functions = self.functions_map.keys()

        # instantiate each class and add it to the class instance for the functions in the constructor
        self.functions = [self.functions_map[function](self) for function in functions]
