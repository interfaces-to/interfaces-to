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
from openai import OpenAI
client = OpenAI()

# 1️⃣ import `into`
import interfaces_to as into

# 2️⃣ add your favourite tools
tools = into.tools(['Slack','OpenAI'])

# 3️⃣ provide some input and start the loop
messages = [{"role": "user", "content": "Introduce yourself in #general and make a joke in #random"}]
while into.running(messages):

  # 4️⃣ create a completion as normal, and run your tools! 🪄
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
  )
  messages = into.run(messages, completion, tools)

# 5️⃣ stand back and watch the magic happen! 🎩✨
print(messages)
```

This prints the following output:

```python
[
    {
        'role': 'user', 
        'content': 'Introduce yourself in #general, make a joke in #random'
    }, 
    {
        'role': 'assistant', 
        'content': None, 
        'tool_calls': [
            {
                'id': 'call_135kkxcrN4OxAQXZinlXGYb', 
                'type': 'function', 
                'function': {
                    'name': 'send_slack_message', 
                    'arguments': '{"channel": "#general", "message": "Hi everyone! I\'m an assistant here to help with tasks and answer questions. Excited to work with you all!"}'
                }
            }, 
            {
                'id': 'call_08ApGj5q8ZyRLuHo10y4FKb', 
                'type': 'function', 
                'function': {
                    'name': 'send_slack_message', 
                    'arguments': '{"channel": "#random", "message": "Why don\'t scientists trust atoms? Because they make up everything!"}'
                }
            }
        ]
    }, 
    {
        'role': 'tool', 
        'content': "Posted message to #general: Hi everyone! I'm an assistant here to help with tasks and answer questions. Excited to work with you all!", 
        'tool_call_id': 'call_135kkxcrN4OxAQXZinlXGYb'
    }, 
    {
        'role': 'tool', 
        'content': "Posted message to #random: Why don't scientists trust atoms? Because they make up everything!", 
        'tool_call_id': 'call_08ApGj5q8ZyRLuHo10y4FKb'
    }, 
    {
        'role': 'assistant', 
        'content': "I've introduced myself in #general and shared a joke in #random! Let me know if you need anything else."
    }
]

```

### Configurating tools

Tools usually require a `token`. Tokens can always be configured by setting the relevant environment variables. e.g. for `Slack` you can set the `SLACK_BOT_TOKEN` environment variable.

If you are using environment variables, you can take advantage of the `into.tools` function to automatically configure your tools. This function will look for the relevant environment variables and configure the tools with default settings.

```python
import interfaces_to as into
tools = into.tools(['Slack'])
```

If you prefer to set the token directly in your code or have more control over tool settings, you can do so by passing arguments to each tool. Tokens provided in code will override any environment variables.

You can optionally restrict `functions` to only those which you need.

Here's an example of configuring the Slack tool:

```python
import interfaces_to as into

tools = [*into.Slack(
    token="xoxb-12345678-xxxxxxxxxx",
    functions=["send_slack_message"]
)]
```

Note that each tool is preceded by an asterisk `*` to unpack the tool's functions into a list, which the OpenAI API SDK expects.

## 📦 Available tools

`into` comes with loads of pre-built tools to help you get started quickly. These tools are designed to be simple, powerful and flexible, and can be used in any combination to create a wide range of applications.

* [Slack](https://interfaces.to/tools/slack):
  * `send_slack_message`: Send a message to a Slack channel
  * `create_channel`: Create a new Slack channel
  * `list_channels`: List all Slack channels with optional filters
  * `read_messages`: Read messages from a Slack channel
  
* [OpenAI](https://interfaces.to/tools/openai):
  * `create_chat_completion` (Create a completion with the OpenAI API)
  * `create_embedding` (Create an embedding with the OpenAI API)

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

We welcome contributions from the community! Please see our [contributing guide](https://interfaces.to/contributing) (coming soon) for more information.

Notable contributors and acknowledgements:

[@blairhudson](https://github.com/blairhudson) &bull; 🐙

## 🫶 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

