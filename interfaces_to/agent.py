from . import read_messages, import_tools, running, run
from .bases import Messages

class Agent:
    def __init__(self, system_message=None, verbose=True):
        self.tools = None
        self.messages = None
        self.first_run = True
        self.completion = None
        self.tools_list = None
        self.messages_list = None
        self.system = {"role":"system","content":system_message} if system_message else None
        self.verbose = verbose

    def add_tools(self, tools_list):
        self.tools_list = tools_list
        return self

    def add_messages(self, input):
        # if messages_list is a string, set self.messages_list directly
        if isinstance(input, str):
            self.messages = [{'role':'user','content':input}]
            return self

        # if messages_list is a list of message objects, set self.messages directly
        if isinstance(input, list) and all(isinstance(message, dict) for message in input):
            self.messages = input
            return self

        self.messages_list = input
        return self

    def __bool__(self):
        if self.messages is None and self.messages_list is not None:
            self.messages = read_messages(self.messages_list)
        if self.tools is None and self.tools_list is not None:
            self.tools = import_tools(self.tools_list)

        if self.first_run and self.system:
            if isinstance(self.messages, Messages):
                self.messages.system = self.system
            else:
                self.messages = [self.system] + self.messages
            

        self.messages = running(self.messages, verbose=self.verbose)
        if self.completion is None and self.first_run:
            self.first_run = False
            return True
        if not self.messages:
            return False
        return True
    
    # when self.completion is set, update the messages
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'completion' and value and not self.first_run:
            self.update_messages()

    def update_messages(self):
        self.messages = run(self.messages, self.completion, self.tools)
        self.completion = None