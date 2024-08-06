import asyncio
from aiohttp import web
import logging
import ngrok
from ..bases import MessageQueue
from ..utils import message_auth

@message_auth(['NGROK_AUTHTOKEN'])
class Ngrok(MessageQueue):
    async def message(self, request):
        try:
            data = await request.text()
            formatted_message = {
                "role": "user",
                "content": f"Respond to the message you received. The message says: {data}"
            }
            self.put_message(formatted_message)
            return web.Response(text="Message received and processed")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return web.Response(text="Failed to process message", status=500)

    def client_thread(self):
        app = web.Application()
        app.add_routes([web.post("/message", self.message)])
        ngrok.set_auth_token(self.token['NGROK_AUTHTOKEN'])

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        runner = web.AppRunner(app)
        loop.run_until_complete(runner.setup())
        listener = ngrok.listen()
        site = web.SockSite(runner, listener)
        loop.run_until_complete(site.start())

        print(f"Listening for POST /message at {listener.url()}\n")
        loop.run_forever()
