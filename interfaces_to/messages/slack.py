import os
import time
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Thread, Event
from queue import Queue

class Slack:
    def __init__(self):
        self.message_queue = Queue()
        self.new_message_event = Event()
        self.slack_app_token = os.environ.get("SLACK_APP_TOKEN")
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        
        if not self.slack_app_token:
            raise ValueError("SLACK_APP_TOKEN environment variable must be set to read messages from Slack")


        if not self.slack_bot_token:
            raise ValueError("SLACK_BOT_TOKEN environment variable must be set to read messages from Slack")
            
        self._start_slack_client()

    def _process_slack_event(self, client: SocketModeClient, req: SocketModeRequest):
        if req.type == "events_api":
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            event = req.payload["event"]
            #if event["type"] == "message" and event.get("subtype") is None:
            bot_user_id = client.web_client.auth_test()['user_id']
            #if event["channel_type"] == "im" or f"<@{bot_user_id}>" in event["text"]:
            formatted_message = {
                "role": "user",
                "content": f"Respond to the message you received from {event['user']} in channel ID {event['channel']}. The message says: {event['text']} "
            }
            self.message_queue.put(formatted_message)
            self.new_message_event.set()

    def _slack_client_thread(self):
        client = SocketModeClient(app_token=self.slack_app_token, web_client=WebClient(token=self.slack_bot_token))
        client.socket_mode_request_listeners.append(self._process_slack_event)
        client.connect()

    def _start_slack_client(self):
        Thread(target=self._slack_client_thread, daemon=True).start()

    def listen(self, messages):
        while True:
            if not messages:
                if self.new_message_event.is_set():
                    self.new_message_event.clear()
                    while not self.message_queue.empty():
                        slack_message = self.message_queue.get()
                        messages.append(slack_message)
            else:
                self.new_message_event.wait()
