
<center><img src="https://github.com/interfaces-to/interfaces-to/raw/main/interfaces-to.png" alt="interfaces.to" width="250" /></center>


# Add a little Action to your LLM Adventure with 🐙 Interfaces

**🐙 Interfaces** (aka `into`) is the quickest way to make Large Language Models _do_ things. It's a simple, powerful and flexible way to build more useful, more engaging and more valuable applications with LLMs.

## ✨ Key Features

⭐️ Built-in tools for common tasks and platforms<br/>
⭐️ Start building with just 4(!) lines of code<br/>
⭐️ Beginner-friendly Python library<br/>
⭐️ Extensible design for custom tools ([example](https://github.com/interfaces-to/interfaces-to/blob/main/interfaces_to/tools/peopledatalabs.py))<br/>
⭐️ Simple and secure configuration<br/>
⭐️ Fully compatible with the OpenAI API SDK<br/>
⭐️ Works with gpt-4o, gpt-4o-mini and other OpenAI models<br/>
⭐️ Works with llama3.1, mistral-large and more via [ollama tools](https://ollama.com/search?c=tools)<br/>
⭐️ Supports (thrives) on `parallel_tool_calls` ([more info](https://platform.openai.com/docs/guides/function-calling/parallel-function-calling)) <br/>
⭐️ Works with any LLM that supports the OpenAI API<br/>
⭐️ Runs on your local machine, in the cloud, or on the edge<br/>
⭐️ Open-source, MIT licensed, and community-driven<br/>

## 🚀 Quick Start

### Installation

Install with pip:
```bash
pip install interfaces-to
```

or

Install with poetry:
```bash
poetry add interfaces-to
```

### Usage

Add your favourite tools to your existing Python project with 4 lines of code:

```python
# 1️⃣ import `into`
import interfaces_to as into

# 2️⃣ import the OpenAI client as normal
from openai import OpenAI
client = OpenAI()

# 3️⃣ add your favourite tools
tools = into.import_tools(['Slack','OpenAI'])

# 4️⃣ provide some input and start the loop
messages = [{"role": "user", "content": "What was the last thing said in each slack channel? Write a 5 line poem to summarise and share it in an appropriate channel"}]
while messages := into.running(messages):

  # 5️⃣ create a completion as normal, and run your tools! 🪄
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
  )
  messages = into.run(messages, completion, tools)

# 6️⃣ stand back and watch the magic happen! 🎩✨
```

This prints the following output:
```python
[user]		  What was the last thing said in each slack channel? Write a 5 line poem to summ
		    arise and share it in an appropriate channel

[assistant]     Calling 1 tool:
		    list_channels({})

[tool]	      Output of tool call list_channels({})
		      Channels: [{'id': 'C07EEUES770', 'name': 'general', 'is_channel':...

[assistant]	  Calling 7 tools:
                read_messages({"channel": "general"})
                read_messages({"channel": "hello"})
                read_messages({"channel": "fun-times"})
                read_messages({"channel": "poetry"})
                read_messages({"channel": "jokes"})
                read_messages({"channel": "welcome"})
                read_messages({"channel": "random"})

[tool]		  Output of tool call read_messages({"channel": "random"})
		    Messages: [{'subtype': 'channel_join', 'user': 'U07ET3LMDB7', ...

[tool]		  Output of tool call read_messages({"channel": "welcome"})
		    Error reading messages: not_in_channel

[tool]		  Output of tool call read_messages({"channel": "jokes"})
		    Messages: [{'user': 'U07EP9STUTU', 'type': 'message', 'ts': '1722477596.990159', ...

[tool]		  Output of tool call read_messages({"channel": "poetry"})
		    Messages: [{'user': 'U07EP9STUTU', 'type': 'message', 'ts':...

[tool]		  Output of tool call read_messages({"channel": "fun-times"})
		    Messages: [{'user': 'U07EP9STUTU', 'type': 'message', 'ts': ...

[tool]		  Output of tool call read_messages({"channel": "hello"})
		    Messages: [{'subtype': 'channel_join', 'user': 'U07EP9STUTU', 'text': '<@U07EP9STUTU> has joined the channel', 'type': 'message', 'ts': '1722421262.722359'}]

[tool]		  Output of tool call read_messages({"channel": "general"})
		    Messages: [{'user': 'U07EP9STUTU', 'type': 'message', 'ts': ...

[assistant]	  Here is a summary poem of the last messages shared in the Slack channels:
		
                In **#general**, they said with glee,
                "Atoms make up all that we see!"
                **#hello** greeted someone new,
                Joining the channel, the greetings flew.
                
                **#fun-times** loved a joke,
                On atoms that can't be broke.
                In the **#poetry** nook, atoms we praised,
                With playful rhymes, our spirits raised.
                
                **#jokes** was all about the spin,
                Electrons in a debate always win.
                And though **#welcome** remained hushed,
                **#random** laughed at atoms crushed.
                
                I'll share this poem in the **#poetry** channel.

[tool]		  Output of tool call send_slack_message({"channel":"poetry","message":"Here's a "...
                Message sent to poetry with timestamp 1722493789.651039: 
                Here's a summary poem of our last messages:
                
                In **#general**, they said with glee,
                "Atoms make up all that we see!"
                **#hello** greeted someone new,
                Joining the channel, the greetings flew.
                
                **#fun-times** loved a joke,
                On atoms that can't be broke.
                In the **#poetry** nook, atoms we praised,
                With playful rhymes, our spirits raised.
                
                **#jokes** was all about the spin,
                Electrons in a debate always win.
                And though **#welcome** remained hushed,
                **#random** laughed at atoms crushed.

[assistant]	  I have shared the poem summarizing the last messages in each channel
                to the **#poetry** channel.
```

`messages` is also updated with the latest messages and retains the format needed by the OpenAI SDK, so you can continue the adventure and build more complex applications.

You can run this example in [this Jupyter notebook](./quickstart.ipynb).

### Configuring tools

#### Using environment variables (Recommended for production)

Tools usually require a `token`. Tokens can always be configured by setting the relevant environment variables. e.g. for `Slack` you can set the `SLACK_BOT_TOKEN` environment variable.

If you are using environment variables, you can take advantage of the `into.import_tools` function to automatically configure your tools. This function will look for the relevant environment variables and configure the tools with default settings.

```python
tools = into.import_tools(['Slack'])
```

#### Using a `.env` file (Recommended for local development)

You can also configure your tools using a `.env` file. This is useful if you want to keep your tokens and other settings in a single file and helpful for local development.

Simply add a `.env` file in the root of your project with the following format:

```env
SLACK_BOT_TOKEN=xoxb-12345678-xxxxxxxxxx
```

#### Setting tokens directly in code

If you prefer to set the token directly in your code or have more control over tool settings, you can do so by passing arguments to each tool. Tokens provided in code will override any environment variables.

You can optionally restrict `functions` to only those which you need.

Here's an example of configuring the Slack tool:

```python
tools = [*into.Slack(
    token="xoxb-12345678-xxxxxxxxxx",
    functions=["send_slack_message"]
)]
```

Note that each tool is preceded by an asterisk `*` to unpack the tool's functions into a list, which the OpenAI API SDK expects.

## 📦 Available tools

`into` comes with loads of pre-built tools to help you get started quickly. These tools are designed to be simple, powerful and flexible, and can be used in any combination to create a wide range of applications.

| Tool | Description | Functions | Configuration |
| --- | --- | --- | --- |
| [Self](https://interfaces.to/tools/self) | Encourage self awareness, time awareness and logical evaluation. | `wait`, `plan`, `get_time`, `do_math` | None required. |
| [OpenAI](https://interfaces.to/tools/openai) | Create completions and embeddings with the OpenAI API (Yes, that means self-prompting 🔥) | `create_chat_completion`, `create_embedding` | Uses `OPENAI_API_KEY` environment variable |
| [Slack](https://interfaces.to/tools/slack) | Send messages to Slack channels, create channels, list channels, and read messages | `send_slack_message`, `create_channel`, `list_channels`, `read_messages` | Uses `SLACK_BOT_TOKEN` environment variable |
| [Notion](https://interfaces.to/tools/notion) | Find, read and create pages in Notion | `search_notion`, `query_notion_database`, `read_notion_page`, `create_notion_page` | Uses `NOTION_TOKEN` environment variable. Databases must be explicitly shared with the integration. |
| [Airtable](https://interfaces.to/tools/airtable) | Find, read and create records in Airtable | `list_all_bases`, `get_base`, `list_base_records`, `create_base_records` | Uses `AIRTABLE_TOKEN` environment variable |
| [People Data Labs](https://interfaces.to/tools/people-data-labs) | Find information about people and companies | `find_person`, `find_company` | Uses `PDL_API_KEY` environment variable |

More tools are coming soon:

* Twilio
* GitHub
* Jira
* Discord
* and more!

See the [🛠️ Tools Project plan](https://github.com/orgs/interfaces-to/projects/1) for more information on upcoming tools.

## 🌐 Experimental: Dynamic messages

`into` supports reading messages dynamically. The `messages` variable required by OpenAI SDK is a list of dictionaries, where each dictionary represents a message. Each message must have a `role` key with a value of either `user` or `assistant`, and a `content` key with the message content.

You can use `into.read_messages` to configure dynamic messages.

```python
messages = into.read_messages(["Slack"])
```

The following sources are currently supported:

| Source | Description | Configuration |
| --- | --- | --- |
| [Slack](https://interfaces.to/messages/slack) | Read messages from a Slack channel where your app is mentioned or in direct messages | Requires `SLACK_APP_TOKEN` and `SLACK_BOT_TOKEN` environment variable. Socket Mode must be enabled with the appropriate events. |
| [Ngrok](https://interfaces.to/messages/ngrok) | Receive POST /message body using Ngrok at https://XXXX-255-255-255-255.ngrok-free.app. Useful for testing webhooks locally. | Requires `NGROK_AUTHTOKEN` environment variable. |
| [FastAPI](https://interfaces.to/messages/fastapi) | Receive POST /message body on Port 8080 with FastAPI. | None required. |
| [CLI](https://interfaces.to/messages/cli) | Read messages from the command line. For use in scripts executed on the command line or with running `into` itself (see below). | None required. |

See the [💬 Messages Project plan](https://github.com/orgs/interfaces-to/projects/3) for more information on upcoming tools.

### Limitations

* Currently only one source can be configured at a time.
* History is not retained between the resolution of messages, however `into` is able to simulate message history by calling the Slack `read_messages` tool if equipped with `into.import_tools(['Slack'])`. 

## 📟 Experimental: CLI Support

`into` supports running tools from the command line. This is useful when `CLI` is the message source, allowing you to run as a standalone application.

By default this uses OpenAI and requires the `OPENAI_API_KEY` environment variable.

You can install `into` with the CLI support by running:

```bash
pipx install interfaces_to
```

and then run and interact with `into` on the command line:

```bash
into --tools=Slack,OpenAI

> Enter the message to be processed: 
```

or run `into` with a message directly via stdin:

```bash
echo "What was the last thing said in each slack channel? Write a 5 line poem to summarise and share it in an appropriate channel" | into --tools=Slack,OpenAI
```

To test out `into` on the command line without installing, clone this repository and run:

```bash
poetry run into --tools=Slack,OpenAI
```

or run `into` with a message directly via stdin:

```bash
echo "What was the last thing said in each slack channel? Write a 5 line poem to summarise and share it in an appropriate channel" | poetry run into --tools=Slack,OpenAI
```

## 📚 Documentation (coming soon!)

For more information, check out the [detailed documentation](https://interfaces.to).

## 💬 Community

Join the [🐙 Interfaces Slack](https://join.slack.com/t/interfacesto/shared_invite/zt-2nocjgn6q-SkrZJ9wppcJLz0Cn9Utw8A) to chat with other LLM adventurers, ask questions, and share your projects.

## 🤝 Contributors (coming soon!)

We welcome contributions from the community! Please see our [contributing guide](./contributing.md) for more information.

Notable contributors and acknowledgements:

[@blairhudson](https://github.com/blairhudson) &bull; 🐙

## 🫶 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

