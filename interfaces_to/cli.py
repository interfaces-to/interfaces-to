import argparse
import os
import json
import sys
from . import import_tools, read_messages, running, run

def main():
    parser = argparse.ArgumentParser(description='Run interfaces_to with specified tools.')
    parser.add_argument('--tools', required=True, help='Comma-separated list of tools to use, e.g., --tools=Slack,OpenAI')
    parser.add_argument('--messages', default='CLI', help='Comma-separated list of message sources, default is CLI')
    parser.add_argument('--model', default='gpt-4o', help='Model to use, default is gpt-4o')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--azure', action='store_true', help='Switch to Azure OpenAI')
    parser.add_argument('--endpoint', help='Change the OpenAI endpoint, e.g., for use with Ollama')
    parser.add_argument('--all', action='store_true', help='Output all messages, default is to output only the last message')

    parser.add_argument('message', nargs='?', help='Optional message to be pushed via stdin when messages=CLI')
    args = parser.parse_args()

    tools_input = args.tools.split(',')

    tools = import_tools(tools_input)

    if args.azure:
        from openai import AzureOpenAI
        api_key = args.api_key or os.getenv("AZURE_OPENAI_API_KEY")
        if not api_key:
            raise ValueError("--api-key or AZURE_OPENAI_API_KEY must be provided")
        azure_endpoint = args.endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        if not azure_endpoint:
            raise ValueError("--endpoint or AZURE_OPENAI_ENDPOINT must be provided")
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-12-01-preview",
            azure_endpoint=azure_endpoint
        )
    else:
        from openai import OpenAI
        client = OpenAI(
            api_key=args.api_key or os.getenv("OPENAI_API_KEY"),
            base_url=args.endpoint
        ) if args.endpoint else OpenAI(api_key=args.api_key or os.getenv("OPENAI_API_KEY"))

    if args.messages == 'CLI' and args.message:
        messages = [{"role": "user", "content": args.message}]
        # suppress stdout
        sys.stdout = open(os.devnull, 'w')
    else:
        messages_sources = args.messages.split(',')
        messages = read_messages(messages_sources)

    final_messages = []
    while messages := running(messages):
        completion = client.chat.completions.create(
            model=args.model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        messages = run(messages, completion, tools)
        
        final_messages = messages

    if args.messages == 'CLI' and args.message:
        # restore stdout
        sys.stdout = sys.__stdout__
        if args.all:
            print(json.dumps(final_messages, indent=2))
        else:
            print(json.dumps(final_messages[-1], indent=2))

if __name__ == "__main__":
    main()
