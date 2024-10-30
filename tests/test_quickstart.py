import nbformat
from nbconvert import PythonExporter
import pytest
import os
from unittest.mock import patch

def mock_openai_chat_completions_create(*args, **kwargs):
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Mocked response from OpenAI"
                }
            }
        ]
    }

def mock_slack_api_call(*args, **kwargs):
    return {
        "ok": True,
        "channel": "C1234567890",
        "ts": "1234567890.123456",
        "message": {
            "text": "Mocked Slack message"
        }
    }

@patch('openai.ChatCompletion.create', side_effect=mock_openai_chat_completions_create)
@patch('slack_sdk.WebClient.chat_postMessage', side_effect=mock_slack_api_call)
def test_quickstart_notebook(mock_openai, mock_slack):
    # Load the notebook
    with open("quickstart.ipynb") as f:
        nb = nbformat.read(f, as_version=4)

    # Convert the notebook to a Python script
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)

    # Save the script to a temporary file
    with open("quickstart.py", "w") as f:
        f.write(source)

    # Run the script
    result = os.system("python quickstart.py")

    # Check if the script ran successfully
    assert result == 0, "The quickstart notebook did not run successfully"
