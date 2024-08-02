from .bases import Messages
import json
import importlib

def run(messages, completion, tools, pretty_messages=True):
    tool_map = {json.loads(json.dumps(tool))["function"]["name"]: tool for tool in tools}
    
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

    if pretty_messages:
        # make messages pretty for output from a notebook cell
        return Messages(messages)
    
    return messages

def running(messages, verbose=True) -> bool:
    """If the most recent message is from the user or a tool, return True"""

    if not messages:
        return False
    
    is_running = messages[-1]['role'] in ['user', 'tool']

    # Define ANSI escape codes for colors
    role_colors = {
        'user': '\033[92m',  # Green
        'tool': '\033[94m',  # Blue
        'assistant': '\033[93m',  # Yellow
        'reset': '\033[0m'   # Reset
    }

    def print_message(message, tool_calls_message=None):
        role = message['role']

        # if role is not assistant, add a tab to align the messages
        if role != 'assistant':
            message['content'] = f"\t{message['content']}"

        # add newlines after every 80 characters if role is user or assistant
        if role in ['user', 'assistant'] and message['content']:
            message['content'] = '\n'.join([message['content'][i:i+80] for i in range(0, len(message['content']), 80)])

        # if message contains line breaks, insert 3 tabs to align the messages
        if message['content'] and '\n' in message['content']:
            message['content'] = message['content'].replace('\n', '\n\t\t')

        color = role_colors.get(role, '')
        if message['content'] and message['role'] != 'tool':
            print(f"{color}[{role}]{role_colors['reset']}\t{message['content']}{role_colors['reset']}")

        elif message['content'] and message['role'] == 'tool':
            if tool_calls_message:
                # get tool_calls_message where tool_call_id matches the current message's tool_call_id
                tool_call = next((tool_call for tool_call in tool_calls_message['tool_calls'] if tool_call['id'] == message['tool_call_id']), None)
                print(f"{color}[{role}]{role_colors['reset']}\t\tOutput of tool call {tool_call['function']['name']}({tool_call['function']['arguments']})\n\t{message['content']}{role_colors['reset']}")
            else:
                print(f"{color}[{role}]{role_colors['reset']}\t\t{message['content']}{role_colors['reset']}")
        
        elif message['tool_calls']:
            print(f"{color}[{role}]{role_colors['reset']}\tCalling {len(message['tool_calls'])} tool{'s' if len(message['tool_calls']) > 1 else ''}:")

            for tool_call in message['tool_calls']:
                print(f"\t\t{tool_call['function']['name']}({tool_call['function']['arguments']})")

        print()

    if verbose:

        # get the last message
        message = messages[-1]

        # if the last message is from the user, print it
        if message['role'] in ('user', 'assistant'):
            print_message(message)

        # if the last message is from a tool, print all immediately preceding messages from a tool in the original order
        if message['role'] == 'tool':
            

            to_print = []
            for i, message in enumerate(reversed(messages)):
                if message['role'] == 'tool':
                    to_print.append(message)
                else:
                    break

            if messages[-i-1]['role'] == 'assistant' and messages[-i-1]['tool_calls']:
                print_message(messages[-i-1])

            # get the last message where tool_calls is not None
            tool_calls_message = next((message for message in reversed(messages) if message.get('tool_calls')), None)

            for messages in reversed(to_print):
                if tool_calls_message:
                    print_message(messages, tool_calls_message)
                else:
                    print_message(messages)

            


        
    return is_running



def tools(tool_names=[]):
    """A helper function to import all named tools with default arguments"""

    result = []
    for tool_name in tool_names:
        tool_class = importlib.import_module(f".{tool_name}", package=__package__)
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