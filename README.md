<center>
  <img src="./interfaces-to.png" alt="interfaces.to" width="250" />
</center>

# 🐙 interfaces.to - Add a little Action to your LLM Adventure

**interfaces.to** (aka `into`) is the quickest way to make Large Language Models _do_ things. It's a simple, powerful and flexible way to build more useful, more engaging and more valuable applications with LLMs.

## ✨ Key Features

⭐️ Built-in tools for common tasks and platforms<br/>
⭐️ Start building with just 4(!) lines of code<br/>
⭐️ Developer-friendly Python library<br/>
⭐️ Extensible design for custom tools<br/>
⭐️ Simple and secure configuration<br/>
⭐️ Fully compatible with the OpenAI API SDK<br/>
⭐️ Works with gpt-4o, gpt-4o-mini and other OpenAI models<br/>
⭐️ Works with llama3.1, mistral-large and more via [ollama tools](https://ollama.com/search?c=tools)<br/>
⭐️ Supports (thrives) on `parallel_tool_calls`<br/>
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
tools = into.tools(['Slack','OpenAI'])

# 4️⃣ provide some input and start the loop
messages = [{"role": "user", "content": "What was the last thing said in each slack channel? Write a 5 line poem to summarise and share it in an appropriate channel"}]
while into.running(messages):

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

[assistant]   Calling 1 tool:
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

### Configurating tools

#### Using environment variables (Recommended for production)

Tools usually require a `token`. Tokens can always be configured by setting the relevant environment variables. e.g. for `Slack` you can set the `SLACK_BOT_TOKEN` environment variable.

If you are using environment variables, you can take advantage of the `into.tools` function to automatically configure your tools. This function will look for the relevant environment variables and configure the tools with default settings.

```python
tools = into.tools(['Slack'])
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
| [Self](https://interfaces.to/tools/self) | Encourage self awareness. | `wait` | Not required. |
| [OpenAI](https://interfaces.to/tools/openai) | Create completions and embeddings with the OpenAI API (Yes, that means self-prompting 🔥) | `create_chat_completion`, `create_embedding` | Uses `OPENAI_API_KEY` environment variable |
| [Slack](https://interfaces.to/tools/slack) | Send messages to Slack channels, create channels, list channels, and read messages | `send_slack_message`, `create_channel`, `list_channels`, `read_messages` | Uses `SLACK_BOT_TOKEN` environment variable |
| [Notion](https://interfaces.to/tools/notion) | Find, read and create pages in Notion | `search_notion`, `query_notion_database`, `read_notion_page`, `create_notion_page` | Uses `NOTION_TOKEN` environment variable. Databases must be explicitly shared with the integration. |


Coming soon:

* [GitHub](https://interfaces.to/tools/github):
  * `create_issue`: Create an issue on GitHub
  * `create_pull_request`: Create a pull request on GitHub
  * `create_gist`: Create a gist on GitHub
  * `create_repository`: Create a repository on GitHub
  * `commit_to_repository`: Commit changes to a repository on GitHub
  * `get_repository`: Get a repository on GitHub
  * `search_repositories`: Search for repositories on GitHub
* [Jira](https://interfaces.to/tools/jira):
  * `create_issue`: Create an issue on Jira
  * `assign_issue`: Assign an issue on Jira
  * `transition_issue`: Transition an issue on Jira
  * `comment_on_issue`: Comment on an issue on Jira
  * `get_issue`: Get an issue on Jira
  * `search_issues`: Search for issues on Jira
* [Discord](https://interfaces.to/tools/discord): `send_discord_message` (Send a message to a Discord channel)
* [Telegram](https://interfaces.to/tools/telegram): `send_telegram_message` (Send a message to a Telegram chat)
* [Facebook Messenger](https://interfaces.to/tools/facebook-messenger): `send_facebook_message` (Send a message to a Facebook Messenger chat)
* [WhatsApp](https://interfaces.to/tools/whatsapp): `send_whatsapp_message` (Send a message to a WhatsApp chat)
* [X](https://interfaces.to/tools/x): `post_to_x` (Post on X)
* [Reddit](https://interfaces.to/tools/reddit): `post_to_reddit` (Post on Reddit)
* [Twilio](https://interfaces.to/tools/twilio): `send_sms` (Send an SMS message)
* [SendGrid](https://interfaces.to/tools/sendgrid): `send_email` (Send an email)
* [Mailgun](https://interfaces.to/tools/mailgun): `send_email` (Send an email)
* [Google Sheets](https://interfaces.to/tools/google-sheets): `write_to_sheet` (Write data to a Google Sheet)
* [Google Drive](https://interfaces.to/tools/google-drive): `upload_file` (Upload a file to Google Drive)
* [Google Calendar](https://interfaces.to/tools/google-calendar): `create_event` (Create an event on Google Calendar)
* [Google Maps](https://interfaces.to/tools/google-maps): `get_directions` (Get directions between two locations)
* [Google Search](https://interfaces.to/tools/google-search): `search` (Search the web)
* [Wikipedia](https://interfaces.to/tools/wikipedia): `search` (Search Wikipedia)
* [Weather](https://interfaces.to/tools/weather): `get_weather` (Get the current weather)


## 📚 Documentation (coming soon!)

For more information, check out the [detailed documentation](https://interfaces.to).

## 💬 Community

Join the [interfaces.to Slack](https://join.slack.com/t/interfacesto/shared_invite/zt-2nocjgn6q-SkrZJ9wppcJLz0Cn9Utw8A) to chat with other LLM adventurers, ask questions, and share your projects.

## 🤝 Contributors (coming soon!)

We welcome contributions from the community! Please see our [contributing guide](./contributing.md) for more information.

Notable contributors and acknowledgements:

[@blairhudson](https://github.com/blairhudson) &bull; 🐙

## 🫶 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

