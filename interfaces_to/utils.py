from pydantic import create_model
from typing import get_type_hints
import inspect
from .bases import JSONSerializableFunction, Messages
from docstring_parser import parse
import json
import importlib


def run(messages, completion, tools):
    tool_map = {json.loads(json.dumps(tool))[
        "function"]["name"]: tool for tool in tools}

    for choice in completion.choices:
        if choice.message.content or hasattr(choice.message, 'tool_calls'):
            assistant_message = {
                "role": "assistant",
                "content": choice.message.content,
            }

            # Check if tool_calls is not None and is iterable
            if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
                assistant_message["tool_calls"] = []

                for tool_call in choice.message.tool_calls:
                    assistant_message["tool_calls"].append({
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })

            messages.append(assistant_message)

            if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    tool_name = tool_call.function.name
                    if tool_name in tool_map:
                        tool = tool_map[tool_name]
                        parameters = json.loads(tool_call.function.arguments)
                        result = getattr(tool, tool_name)(**parameters)
                        # Append the tool's action as a message
                        messages.append({
                            "role": "tool",
                            "content": result,
                            "tool_call_id": tool_call.id
                        })

    return messages


def print_message(message):

    # Define ANSI escape codes for colors
    role_colors = {
        'user': '\033[92m',  # Green
        'tool': '\033[94m',  # Blue
        'assistant': '\033[93m',  # Yellow
        'reset': '\033[0m'   # Reset
    }

    tool_calls_message = True if 'tool_calls' in message else False

    role = message['role']

    # if role is not assistant, add a tab to align the messages
    if role != 'assistant':
        message['content'] = f"\t{message['content']}"

    # add newlines after every 80 characters if role is user or assistant
    if role in ['user', 'assistant'] and message['content']:
        message['content'] = '\n'.join(
            [message['content'][i:i+80] for i in range(0, len(message['content']), 80)])

    # if message contains line breaks, insert 3 tabs to align the messages
    if message['content'] and '\n' in message['content']:
        message['content'] = message['content'].replace('\n', '\n\t\t')

    color = role_colors.get(role, '')
    if message['content'] and message['role'] != 'tool':
        print(
            f"{color}[{role}]{role_colors['reset']}\t{message['content']}{role_colors['reset']}")

    elif message['content'] and message['role'] == 'tool':
        if tool_calls_message:
            # get tool_calls_message where tool_call_id matches the current message's tool_call_id
            tool_call = next(
                (tool_call for tool_call in tool_calls_message['tool_calls'] if tool_call['id'] == message['tool_call_id']), None)
            print(f"{color}[{role}]{role_colors['reset']}\t\tOutput of tool call {tool_call['function']['name']}({tool_call['function']['arguments']})\n\t{message['content']}{role_colors['reset']}")
        else:
            print(
                f"{color}[{role}]{role_colors['reset']}\t{message['content']}{role_colors['reset']}")

    elif message['tool_calls']:
        print(f"{color}[{role}]{role_colors['reset']}\tCalling {len(message['tool_calls'])} tool{'s' if len(message['tool_calls']) > 1 else ''}:")

        for tool_call in message['tool_calls']:
            # add tabs to tool_call['function']['arguments'] if it contains line breaks
            tool_call['function']['arguments'] = tool_call['function']['arguments'].replace(
                '\n', '\n\t\t')

            print(
                f"\t\t{tool_call['function']['name']}({tool_call['function']['arguments']})")

    print()


def running(messages, verbose=True) -> bool:
    """If the most recent message is from the user or a tool, return True"""

    if not messages:
        is_running = False
    else:
        # is running if last role is user, tool, or assistant but with tool_calls
        is_running = messages[-1]['role'] in ['user', 'tool'] or (messages[-1]['role'] == 'assistant' and 'tool_calls' in messages[-1])

    # if verbose and type of messages is not .bases Messagesm, make messages = Messages(messages)
    if verbose:
        if not isinstance(messages, Messages):       
            messages = Messages(messages, verbose=True, print_fn=print_message)
            for message in messages:
                messages.print_fn(message)
        else:
            messages.verbose = True
            messages.print_fn = print_message

    if is_running:
        return messages
    elif isinstance(messages, Messages) and messages.listeners:
        # we need wait to listen for messages
        messages.clear_if_finished()
        messages.block_if_empty()
        return messages
    else:
        return False


def import_tools(tool_names=[], include_self=True):
    """A helper function to import all named tools with default arguments. 
    Self is included by default, but can be excluded by setting include_self=False"""

    result = []
    for tool_name in tool_names:
        tool_class = importlib.import_module(
            f".{tool_name}", package=__package__)
        result.extend(tool_class())

    if include_self and 'Self' not in tool_names:
        tool_class = importlib.import_module(
            ".Self", package=__package__)
        result.extend(tool_class())

    return result


class LazyImport:
    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name
        self._class = None

    def _load_class(self):
        module = importlib.import_module(self.module_name, package=__package__)
        self._class = getattr(module, self.class_name)

    def __getattr__(self, item):
        if self._class is None:
            self._load_class()
        return getattr(self._class, item)

    def __call__(self, *args, **kwargs):
        if self._class is None:
            self._load_class()
        return self._class(*args, **kwargs)


def method_to_json_schema(method):
    signature = inspect.signature(method)
    hints = get_type_hints(method)
    hints.pop('return', None)  # Remove return type hint if present
    hints.pop('self', None)  # Remove 'self' from type hints
    model_fields = {name: (typ, ...) for name,
                    typ in hints.items() if name in signature.parameters}
    dynamic_model = create_model('DynamicModel', **model_fields)
    return dynamic_model.schema()


def callable_function(func):

    func._callable = True

    class CallableFunction(JSONSerializableFunction):

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"

            # print the func parameters, type hints, and defaults
            signature = inspect.signature(func)
            func_parameters = signature.parameters

            # check that the function has a docstring
            if not func.__doc__:
                raise ValueError(
                    f"Missing docstring for function {func.__name__} in {func.__module__}")

            docstring = parse(func.__doc__)
            params = {param.arg_name: param for param in docstring.params}

            # check that docstring has a description
            if not docstring.description:
                raise ValueError(
                    f"Missing description for function {func.__name__} in {func.__module__}")

            # check that all parameters have a description
            for parameter in func_parameters.values():
                if parameter.name == 'self':
                    continue
                if parameter.name not in params:
                    raise ValueError(
                        f"Missing description for parameter {parameter.name} in function {func.__name__}")

            # check that all parameters have a type hint
            for parameter in func_parameters.values():
                if parameter.name == 'self':
                    continue
                if parameter.annotation == inspect.Parameter.empty:
                    raise ValueError(
                        f"Missing type hint for parameter {parameter.name} in function {func.__name__}")

            # generate JSON schema for the function parameters
            parameters = method_to_json_schema(func)

            # add descriptions from docstring to parameters
            for parameter in parameters['properties']:
                if parameter in params:
                    parameters['properties'][parameter]['description'] = params[parameter].description

            self['function'] = {
                "name": func.__name__,
                "description": docstring.description,
                "parameters": parameters
            }

    # add func to the class with the same name
    setattr(CallableFunction, func.__name__, func)

    func._class = CallableFunction
    return func


def tool_auth(*, token_env_name):
    def decorator(cls):
        cls.token_env_name = token_env_name
        return cls
    return decorator

def read_messages(listener_names=[]):

    if not listener_names:
        raise ValueError("You must specify at least one listener")

    if len(listener_names) > 1:
        raise NotImplementedError(
            "More than one listener is not yet supported")

    try:
        listeners = []
        for listener_name in listener_names:
            listener_class = importlib.import_module(
                f".{listener_name}", package=f"{__package__}.messages")
            listeners.append(listener_class().listen)

        return Messages(listeners=listeners)
    except ModuleNotFoundError as e:
        raise ValueError(f"Listener {listener_name} not found.") from e