from ..bases import FunctionSet, JSONSerializableFunction
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class Slack(FunctionSet):

    class SlackFunction(JSONSerializableFunction):

        def _join_channel(self, channel_id):
            client = WebClient(token=self.tool.token)
            try:
                response = client.conversations_join(channel=channel_id)
                return f"Joined channel {channel_id}"
            except SlackApiError as e:
                return f"Error joining channel: {e.response['error']}"
            
        def _get_channels(self):
            client = WebClient(token=self.tool.token)
            try:
                response = client.conversations_list()
                channels = response["channels"]
                return channels
            except SlackApiError as e:
                return f"Error retrieving channels: {e.response['error']}"

    class ReadMessages(SlackFunction):

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "read_messages",
                "description": "Read messages from a Slack channel",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel_name": {
                            "type": "string",
                            "description": "The Slack channel, e.g. general. Always omit the # symbol",
                        },
                        "channel_id": {
                            "type": "string",
                            "description": "The ID of the Slack channel, e.g. C07EEUES770.",
                        },
                    },
                },
            }

        def read_messages(self, channel_name="", channel_id=""):
            client = WebClient(token=self.tool.token)
            try:
                channels = self._get_channels()
                _channel = None
                if channel_name != "":
                    for c in channels:
                        if c["name"] == channel_name:
                            _channel = c
                    channel_id = _channel["id"]
                if channel_id == "":
                    return f"Error reading messages: must provide channel name or channel id"
                response = client.conversations_history(channel=channel_id)
                messages = response["messages"]
                return f"Messages: {messages}"
            except SlackApiError as e:
                return f"Error reading messages: {e.response['error']}"
        

    class CreateChannel(SlackFunction):
            
        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "create_channel",
                "description": "Create a new Slack channel",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "The name of the channel to create",
                        },
                    },
                    "required": ["channel"],
                },
            }

        def create_channel(self, channel):
            client = WebClient(token=self.tool.token)
            try:
                response = client.conversations_create(name=channel)
                return f"Channel {channel} created with ID {response['channel']['id']}"
            except SlackApiError as e:
                return f"Error creating channel: {e.response['error']}"
    
    class ListChannels(SlackFunction):
        """List all channels in the workspace with optional search filter"""

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "list_channels",
                "description": "Find a channel for a specific purpose. List all channels in the workspace with optional search filter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search": {
                            "type": "string",
                            "description": "Optional search filter to apply to the channel list",
                        },
                    },
                },
            }

        def list_channels(self, search=None):
            client = WebClient(token=self.tool.token)
            try:
                response = client.conversations_list()
                channels = response["channels"]
                if search:
                    channels = [c for c in channels if search in c["name"]]
                # return the list of channels as a string
                return f"Channels: {channels}"
            except SlackApiError as e:
                return f"Error listing channels: {e.response['error']}"

    class SendSlackMessage(SlackFunction):

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "send_slack_message",
                "description": "Send a message to a Slack channel",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel_name": {
                            "type": "string",
                            "description": "The Slack channel name, e.g. general. Always omit the # symbol",
                        },
                        "channel_id": {
                            "type": "string",
                            "description": "The ID of the Slack channel e.g. C07EEUES770"
                        },
                        "message": {
                            "type": "string",
                            "description": "The message to send to the Slack channel"
                        },
                    },
                    "required": ["message"],
                },
            }

        def send_slack_message(self,  message, channel_name="", channel_id=""):
            client = WebClient(token=self.tool.token)

            # get channels
            channels = self._get_channels()

            # check if channel exists
            _channel = None
            if channel_name != "":
                for c in channels:
                    if c["name"] == channel_name:
                        _channel = c
                channel_id = _channel["id"]
            if channel_id == "":
                return f"Error reading messages: must provide channel name or channel id"

            if channel_id == "":
                return f"Channel {channel_id} not found"

            for c in channels:
                if c["id"] == channel_id:
                    _channel = c

            # join if not member
            # if not _channel['is_member']:
            #     self._join_channel(_channel['id'])

            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=message
                )
                return f"Message sent to {channel_id} with timestamp {response['ts']}: {message}"
            except SlackApiError as e:
                return f"Error sending message: {e.response['error']}"


    def __init__(self, token=None, functions=None):
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
            'create_channel': Slack.CreateChannel,
            'list_channels': Slack.ListChannels,
            'read_messages': Slack.ReadMessages,
        }

        if functions is None:
            functions = self.functions_map.keys()

        # instantiate each class and add it to the class instance for the functions in the constructor
        self.functions = [self.functions_map[function](self) for function in functions]
