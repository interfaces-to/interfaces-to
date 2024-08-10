import argparse
import os
import json
import sys
from . import Agent
from openai import OpenAI, AzureOpenAI

def main():
    parser = argparse.ArgumentParser(description='Run interfaces_to with specified tools.')
    parser.add_argument('--tools', default="Self", help='Comma-separated list of tools to use, e.g., --tools=Slack,OpenAI')
    parser.add_argument('--messages', default='CLI', help='Comma-separated list of message sources, default is CLI')
    parser.add_argument('--model', default='gpt-4o', help='Model to use, default is gpt-4o')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--azure', action='store_true', help='Switch to Azure OpenAI')
    parser.add_argument('--endpoint', help='Change the OpenAI endpoint, e.g., for use with Ollama')
    parser.add_argument('--all', action='store_true', help='Output all messages, default is to output only the last message')
    parser.add_argument('--system', default=None, help='Optional system message to initialize the agent')

    parser.add_argument('message', nargs='?', help='Optional message to be pushed via stdin when messages=CLI')
    args = parser.parse_args()

    tools_input = args.tools.split(',')

    if args.azure:
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
        client = OpenAI(
            api_key=args.api_key or os.getenv("OPENAI_API_KEY"),
            base_url=args.endpoint
        ) if args.endpoint else OpenAI(api_key=args.api_key or os.getenv("OPENAI_API_KEY"))

    if args.messages:
        args.messages = args.messages.split(',')
    
    if 'CLI' in args.messages:
        if args.message:
            sys.stdout = open(os.devnull, 'w')
        elif not sys.stdin.isatty():
            sys.stdout = open(os.devnull, 'w')
            args.message = sys.stdin.read().strip()

    if args.system:
        agent = Agent(args.system, verbose=False if args.message else True).add_tools(tools_input)
    else:
        agent = Agent(verbose=False if args.message else True).add_tools(tools_input)

    if args.message:
        agent.add_messages(args.message)
    else:
        agent.add_messages(args.messages)

    final_messages = []
    while agent:
        agent.completion = client.chat.completions.create(
            model=args.model,
            messages=agent.messages,
            tools=agent.tools,
            tool_choice="auto"
        )
        
        final_messages = agent.messages

    if 'CLI' in args.messages and args.message:
        sys.stdout = sys.__stdout__
        if args.all:
            print(json.dumps(final_messages, indent=2))
        else:
            print(json.dumps(final_messages[-1], indent=2))

if __name__ == "__main__":
    main()
