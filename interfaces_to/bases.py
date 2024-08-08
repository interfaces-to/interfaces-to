from threading import Event, Thread
import threading
from queue import Queue
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
            function.__name__: self._inject_token(function._class, self.token)
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

    def _inject_token(self, cls, token):
        cls.token = token
        return cls


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
            for listener in listeners:
                threading.Thread(target=listener.listen, args=(
                    self,), daemon=True).start()

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


class MessageQueue:
    def __init__(self):
        self.message_queue = Queue()
        self.new_message_event = Event()
        self.start_client()

    def put_message(self, message):
        self.message_queue.put(message)
        self.new_message_event.set()

    def listen(self, messages):
        while True:
            if not messages:
                if self.new_message_event.is_set():
                    self.new_message_event.clear()
                    while not self.message_queue.empty():
                        incoming_message = self.message_queue.get()
                        messages.append(incoming_message)
            else:
                self.new_message_event.wait()

    def client_thread(self):
        raise NotImplementedError("Subclasses should implement this method")

    def start_client(self):
        Thread(target=self.client_thread, daemon=True).start()