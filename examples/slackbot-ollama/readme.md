# Build a Slackbot with 🐙 Interfaces with Llama3.1

🐙 Interfaces works with open source models too! This example will show you have to build a Slackbot with Llama3.

**Note:** Running Large Language Models on your local machine can be resource intensive. The performance of the model may vary depending on your hardware.

## Setup

### Setting up Slack

You will need to configure your Slack app and OpenAI API key as described in the [Slackbot with 🐙 Interfaces](../slackbot/readme.md) example.

### Running Llama3.1

1. Download and install Ollama from [https://ollama.com/download](https://ollama.com/download)
2. Run `ollama run llama3.1:8b` to download and run Llama3.1 model

### Running the Slackbot

1. Install dependencies with `pip install interfaces-to slack_sdk`
2. Update your environment variables in `.env`
3. Run it with `python slackbot-ollama.py`

See [slackbot-ollama.py](slackbot-ollama.py) for the full code.

## Using other models

Ollama supports a variety of models. You can run any of the models by changing the model name in the `ollama run` command and updating the `model` parameter in the `completion` function in `slackbot-ollama.py` on Line 16.

**Important:** The model must support function calls to work with 🐙 Interfaces, otherwise tools will not be used. These include:

* [llama3.1](https://ollama.com/library/llama3.1)
* mistral models: [mistral-nemo](https://ollama.com/library/mistral-nemo), [mistral-large](https://ollama.com/library/mistral-large), [mistral](https://ollama.com/library/mistral), [mixtral](https://ollama.com/library/mixtral)
* [command-r-plus](https://ollama.com/library/command-r-plus)
* [fire-function-v2](https://ollama.com/library/firefunction-v2)

You can view all supported models [here](https://ollama.com/search?c=tools).