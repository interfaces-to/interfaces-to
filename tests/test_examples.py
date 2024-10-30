import os
import subprocess
import pytest
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
def test_cli_script(mock_openai, mock_slack):
    # Set up environment variables
    os.environ['SLACK_BOT_TOKEN'] = 'xoxb-12345678-xxxxxxxxxx'
    
    # Run the cli.sh script
    result = subprocess.run(['bash', 'examples/cli/cli.sh'], capture_output=True, text=True)
    
    # Check if the script ran successfully
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    
    # Check if the output file is created
    assert os.path.exists('examples/cli/output.txt'), "Output file not created"
    
    # Check the content of the output file
    with open('examples/cli/output.txt', 'r') as file:
        content = file.read()
        assert content.strip() != "", "Output file is empty"

@patch('openai.ChatCompletion.create', side_effect=mock_openai_chat_completions_create)
@patch('slack_sdk.WebClient.chat_postMessage', side_effect=mock_slack_api_call)
def test_slackbot_script(mock_openai, mock_slack):
    # Set up environment variables
    os.environ['SLACK_BOT_TOKEN'] = 'xoxb-12345678-xxxxxxxxxx'
    os.environ['OPENAI_API_KEY'] = 'sk-12345678'
    
    # Run the slackbot.py script
    result = subprocess.run(['python', 'examples/slackbot/slackbot.py'], capture_output=True, text=True)
    
    # Check if the script ran successfully
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    
    # Check if the script produced the expected output
    assert "Mocked response from OpenAI" in result.stdout, "Expected output not found in script output"

@patch('openai.ChatCompletion.create', side_effect=mock_openai_chat_completions_create)
@patch('slack_sdk.WebClient.chat_postMessage', side_effect=mock_slack_api_call)
def test_slackbot_ollama_script(mock_openai, mock_slack):
    # Set up environment variables
    os.environ['SLACK_BOT_TOKEN'] = 'xoxb-12345678-xxxxxxxxxx'
    
    # Run the slackbot-ollama.py script
    result = subprocess.run(['python', 'examples/slackbot-ollama/slackbot-ollama.py'], capture_output=True, text=True)
    
    # Check if the script ran successfully
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    
    # Check if the script produced the expected output
    assert "Mocked response from OpenAI" in result.stdout, "Expected output not found in script output"
