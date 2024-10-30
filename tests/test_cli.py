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
def test_into_command(mock_openai, mock_slack):
    # Set up environment variables
    os.environ['SLACK_BOT_TOKEN'] = 'xoxb-12345678-xxxxxxxxxx'
    os.environ['OPENAI_API_KEY'] = 'sk-12345678'
    
    # Run the into command with a sample input
    result = subprocess.run(['into', '--tools=Slack', '--model=gpt-4o', 'What is the time?'], capture_output=True, text=True)
    
    # Check if the command ran successfully
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    
    # Check if the output is not empty
    assert result.stdout.strip() != "", "Command output is empty"

@patch('openai.ChatCompletion.create', side_effect=mock_openai_chat_completions_create)
@patch('slack_sdk.WebClient.chat_postMessage', side_effect=mock_slack_api_call)
def test_into_command_with_system_message(mock_openai, mock_slack):
    # Set up environment variables
    os.environ['SLACK_BOT_TOKEN'] = 'xoxb-12345678-xxxxxxxxxx'
    os.environ['OPENAI_API_KEY'] = 'sk-12345678'
    
    # Run the into command with a system message
    result = subprocess.run(['into', '--tools=Slack', '--model=gpt-4o', '--system=translate to french', 'Hello, how are you?'], capture_output=True, text=True)
    
    # Check if the command ran successfully
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    
    # Check if the output is not empty
    assert result.stdout.strip() != "", "Command output is empty"

@patch('openai.ChatCompletion.create', side_effect=mock_openai_chat_completions_create)
@patch('slack_sdk.WebClient.chat_postMessage', side_effect=mock_slack_api_call)
def test_into_command_with_stdin(mock_openai, mock_slack):
    # Set up environment variables
    os.environ['SLACK_BOT_TOKEN'] = 'xoxb-12345678-xxxxxxxxxx'
    os.environ['OPENAI_API_KEY'] = 'sk-12345678'
    
    # Run the into command with input from stdin
    result = subprocess.run(['echo', 'Hello, how are you?', '|', 'into', '--tools=Slack', '--model=gpt-4o'], capture_output=True, text=True, shell=True)
    
    # Check if the command ran successfully
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    
    # Check if the output is not empty
    assert result.stdout.strip() != "", "Command output is empty"
