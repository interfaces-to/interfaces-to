import gradio as gr
from ..bases import MessageQueue

class Gradio(MessageQueue):

    def receive_message(self, message):
        self.history.append({"role": message['role'], "content": message['content']})
        return super().receive_message(message)

    def start_client(self):

        def respond_to_message(message, history):
            formatted_message = {
                "role": "user",
                "content": f"{message}"
            }
            self.put_message(formatted_message)
            # Adding the response to the history in the correct format
            return "", history

        def update_chat_interface():
            # Ensure no None values are in the messages
            formatted_history = [{"role": msg["role"], "content": msg["content"] if msg["content"] is not None else f"{msg.get('tool_calls','')}"} for msg in self.history]
            return formatted_history

        with gr.Blocks() as self.chat_interface:
            self.history = []
            chatbot = gr.Chatbot(type="messages",value=update_chat_interface,every=1, layout='panel')  # Set type to 'messages'
            msg = gr.Textbox(label="Enter a message")
            clear = gr.Button("Clear")


            #self.chat_interface.load(fn=update_chat_interface, every=1, outputs=chatbot)

            msg.submit(fn=respond_to_message, inputs=[msg, chatbot], outputs=[msg, chatbot])
            clear.click(fn=lambda: ([], []), outputs=[msg, chatbot])

        self.chat_interface.launch(share=True, prevent_thread_lock=True)
