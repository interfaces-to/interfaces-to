from .bases import Messages
import json

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

    if verbose:
        # Print the last message and any immediately preceding with the same role
        for message in reversed(messages):
            role = message['role']

            # if role is not assistant, add a tab to align the messages
            if role != 'assistant':
                message['content'] = f"\t{message['content']}"

            # add newlines after every 80 characters if role is user or assistant
            if role in ['user', 'assistant']:
                message['content'] = '\n'.join([message['content'][i:i+80] for i in range(0, len(message['content']), 80)])

            # if message contains line breaks, insert 3 tabs to align the messages
            if message['content'] and '\n' in message['content']:
                message['content'] = message['content'].replace('\n', '\n\t\t')

            color = role_colors.get(role, '')
            print(f"{color}[{role}]{role_colors['reset']}\t{message['content'] or message['tool_calls']}{role_colors['reset']}")
            if role != list(reversed(messages))[-1]['role']:
                break
        
    return is_running


def tools(tool_names=[]) -> list[str]:
    """A helper function to import all named tools with default arguments"""

    result = []
    for tool_name in tool_names:
        module = __import__(__name__.split('.')[0], fromlist=[tool_name])
        result.extend(getattr(module, tool_name)())
    return result

