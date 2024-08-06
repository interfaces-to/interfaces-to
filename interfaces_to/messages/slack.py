from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from ..bases import MessageQueue
from ..utils import message_auth

@message_auth(['SLACK_APP_TOKEN', 'SLACK_BOT_TOKEN'])
class Slack(MessageQueue):
    def _process_slack_event(self, client: SocketModeClient, req: SocketModeRequest):
        if req.type == "events_api":
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            event = req.payload["event"]
            bot_user_id = client.web_client.auth_test()['user_id']
            if not event.get("user") == bot_user_id:
                formatted_message = {
                    "role": "user",
                    "content": f"Respond to the message you received from {event['user']} in channel ID {event['channel']}. The message says: {event['text']} "
                }
                self.put_message(formatted_message)

    def client_thread(self):
        client = SocketModeClient(app_token=self.token['SLACK_APP_TOKEN'], web_client=WebClient(token=self.token['SLACK_BOT_TOKEN']))
        client.socket_mode_request_listeners.append(self._process_slack_event)
        client.connect()