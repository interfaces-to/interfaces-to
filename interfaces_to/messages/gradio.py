from gradio import ChatInterface
from ..bases import MessageQueue

class Gradio(MessageQueue):
    
    def start_client(self):

        def respond_to_message(message, history):
            formatted_message = {
                "role": "user",
                "content": f"Respond to the message you received. The message says: {message}"
            }
            self.put_message(formatted_message)
            return "Message received and processed"

        chat_interface = ChatInterface(
            fn=respond_to_message,
            title="Chat with the Bot",
            description="Enter your message below:"
        )
        chat_interface.launch(share=True, prevent_thread_lock=True)  # `share=True` ensures the interface is accessible
