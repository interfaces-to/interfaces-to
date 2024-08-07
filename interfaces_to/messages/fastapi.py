import logging
from fastapi import FastAPI as FastAPIBase, Request, HTTPException
from ..bases import MessageQueue
#from ..utils import message_auth
import uvicorn

#@message_auth(['FASTAPI_AUTHTOKEN'])
class FastAPI(MessageQueue):
    def __init__(self):
        super().__init__()
        self.app = FastAPIBase()

        @self.app.post("/message")
        async def message(request: Request):
            try:
                data = await request.body()
                formatted_message = {
                    "role": "user",
                    "content": f"Respond to the message you received. The message says: {data.decode('utf-8')}"
                }
                self.put_message(formatted_message)
                return {"message": "Message received and processed"}
            except Exception as e:
                logging.error(f"Error processing message: {e}")
                raise HTTPException(status_code=500, detail="Failed to process message")

    def client_thread(self):
        print("Listening on http://0.0.0.0:8080")
        uvicorn.run(self.app, host="0.0.0.0", port=8080)
