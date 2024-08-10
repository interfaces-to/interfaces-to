# Add Agents to your CLI scripts with 🐙 Interfaces

Interfaces provides a powerful CLI mode that lets you bring LLM agents to your terminal. This is a great way to automate tasks, build scripts, and even create your own CLI tools.

## Installation

To get started, you need to install the `interfaces-to` package. You can do this using pipx. 

Install pipx if you haven't already with `pip install pipx`. Make sure that pipx is on your PATH with `pipx ensurepath`.

Then you can install `interfaces-to` with the following command:

```bash
pipx install interfaces-to
```

You will need the optional dependencies for the tools you want to use. For example, if you want to use the `Slack` tool, instead install with:

```bash
pipx install interfaces-to[slack]
```

If you need to add a tool later, you can do so with:

```bash
pipx inject interfaces-to notion
```

## Usage

You can now run Interfaces on the command line with the `into` command. 

### Interactive mode

To start an interactive session, run:

```bash
into
```

You can optionally add a tool to start with:

```bash
into --tools=slack
```

### Non-interactive mode

You can also run a single command with:

```bash
into "hello world"
```

This will output the result of the command to the terminal in JSON format.

You can also pipe a message into the command:

```bash
echo "hello world" | into
```

This is useful for chaining commands together, such as input from a file or another command and output to `jq` for processing.

You can combine tools and a system message for more complex commands:

```bash
cat input.txt | into --tools=slack --system="translate to french" | jq -r '.content' > output.txt
```

See [cli.sh](cli.sh) for a multi-step example.
