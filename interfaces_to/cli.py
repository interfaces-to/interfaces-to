
import argparse
from . import import_tools, read_messages, running, run


def main():
    parser = argparse.ArgumentParser(description='Run interfaces_to with specified tools.')
    parser.add_argument('--tools', required=True, help='Comma-separated list of tools to use, e.g., --tools=Slack,OpenAI')
    args = parser.parse_args()

    tools_input = args.tools.split(',')

    tools = import_tools(tools_input)

    from openai import OpenAI
    client = OpenAI()

    messages = read_messages(['CLI'])

    while messages := running(messages):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        messages = run(messages, completion, tools)

if __name__ == "__main__":
    main()