import logging
from ..bases import MessageQueue


class CLI(MessageQueue):
    def client_thread(self):
        while not self.exit_event.is_set():
            self.ready_for_input.wait()
            if self.ready_for_input.is_set():
                message = input("Enter the message to be processed: ")
                    
                try:
                    formatted_message = {
                        "role": "user",
                        "content": f"{message}"
                    }
                    self.put_message(formatted_message)
                    self.ready_for_input.clear()
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

