import logging
from ..bases import MessageQueue


class CLI(MessageQueue):


    def client_thread(self):
        message = input("Enter the message to be processed: ")

        try:
            formatted_message = {
                "role": "user",
                "content": f"{message}"
            }
            self.put_message(formatted_message)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
