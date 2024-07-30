from ..bases import FunctionSet, JSONSerializableFunction
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class Slack(FunctionSet):

    class SendSlackMessage(JSONSerializableFunction):

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "send_slack_message",
                "description": "Send a message to a Slack channel",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "The Slack channel, e.g. general. Always omit the # symbol",
                        },
                        "message": {
                            "type": "string",
                            "description": "The message to send to the Slack channel",
                        },
                    },
                    "required": ["channel", "message"],
                },
            }

        def _join_channel(self, channel_id):
            client = WebClient(token=self.tool.token)
            try:
                response = client.conversations_join(channel=channel_id)
                print(f"Joined channel {channel_id}")
                return f"Joined channel {channel_id}"
            except SlackApiError as e:
                print(f"Error joining channel: {e.response['error']}")
                return f"Error joining channel: {e.response['error']}"
            
        def _get_channels(self):
            client = WebClient(token=self.tool.token)
            try:
                response = client.conversations_list()
                print(response)
                channels = response["channels"]
                return channels
            except SlackApiError as e:
                print(f"Error retrieving channels: {e.response['error']}")
                return None

        def send_slack_message(self, channel, message):
            client = WebClient(token=self.tool.token)

            # get channels
            channels = self._get_channels()

            # check if channel exists
            _channel = None
            for c in channels:
                if c["name"] == channel:
                    _channel = c

            if not _channel:
                print(f"Channel {channel} not found")
                return f"Channel {channel} not found"
            
            # join if not member
            if not _channel['is_member']:
                self._join_channel(_channel['id'])

            try:
                response = client.chat_postMessage(
                    channel=_channel['id'],
                    text=message
                )
                print(f"Message sent to {channel} with timestamp {response['ts']}: {message}")
                return f"Message sent to {channel} with timestamp {response['ts']}: {message}"
            except SlackApiError as e:
                print(f"Error sending message: {e.response['error']}")
                return f"Error sending message: {e.response['error']}"


    def __init__(self, token=None, functions=['send_slack_message']):
        self.token = token

        # try and load token from os.environ["SLACK_BOT_TOKEN"]
        if token is None:
            try:
                self.token = os.environ["SLACK_BOT_TOKEN"]
            except KeyError:
                raise ValueError("No token provided and SLACK_BOT_TOKEN not found in environment variables")

        # create a manual mapping of function names to classes
        self.functions_map = {
            'send_slack_message': Slack.SendSlackMessage,
        }

        # instantiate each class and add it to the class instance for the functions in the constructor
        self.functions = [self.functions_map[function](self) for function in functions]
