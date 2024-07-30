from ..bases import FunctionSet, JSONSerializableFunction
from openai import OpenAI
import os

class OpenAITool(FunctionSet):

    class CreateChatCompletion(JSONSerializableFunction):

        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
            "name": "create_chat_completion",
            "description": "Create a completion using the OpenAI API",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to use for completion",
                    },
                    "model": {
                        "type": "string",
                        "description": "The model to use for completion. e.g. gpt-4o",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "The optional system prompt to use to guide the model. e.g. You are a helpful assistant.",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "The maximum number of tokens to generate",
                    },
                },
                "required": ["prompt"],
            },
        }
            
        def create_chat_completion(self, prompt, model="gpt-4o", system_prompt="You are a helpful assistant.", max_tokens=None):
            client = OpenAI(api_key=self.tool.token)
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens
            )
            response = completion.choices[0].message.content

            print(f"Created completion using model {model} with prompt {prompt} and max tokens {max_tokens}. Response: {response}")
            return f"Created completion using model {model} with prompt {prompt} and max tokens {max_tokens}. Response: {response}"

    
    def __init__(self, token=None, functions=['create_chat_completion']):
        self.token = token

        # try and load the token from the environment
        if token is None:
            try:
                self.token = os.environ['OPENAI_API_KEY']
            except KeyError:
                raise ValueError("No token provided and OPENAI_API_KEY not found in environment")

        # create a manual mapping of function names to classes
        self.functions_map = {
            'create_chat_completion': self.CreateChatCompletion,
        }

        # instantiate each class and add it to the class instance for the functions in the constructor
        self.functions = [self.functions_map[function](self) for function in functions]