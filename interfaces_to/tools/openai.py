from ..bases import FunctionSet
from ..utils import callable_function, tool_auth
from openai import OpenAI as OpenAISDK

@tool_auth(token_env_name='OPENAI_API_KEY')
class OpenAI(FunctionSet):

    @callable_function
    def create_chat_completion(self, prompt: str, model: str = "gpt-4o", system_prompt: str = "You are a helpful assistant.", max_tokens: int = None):
        """
        Create a completion using the OpenAI API
        
        :param prompt: The prompt to use for completion
        :param model: The model to use for completion. e.g. gpt-4o
        :param system_prompt: The optional system prompt to use to guide the model. e.g. You are a helpful assistant.
        :param max_tokens: The maximum number of tokens to generate
        """
        client = OpenAISDK(api_key=self.token)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens
        )
        response = completion.choices[0].message.content

        return f"Created completion using model {model} with prompt {prompt} and max tokens {max_tokens}. Response: {response}"
    
    @callable_function
    def create_embedding(self, input: str, model: str = "text-embedding-3-large"):
        """
        Create an embedding using the OpenAI API. Embeddings are vectors that represent the meaning of text.
        
        :param input: The text to embed
        :param model: The model to use for completion. e.g. text-embedding-3-large or text-embedding-3-small
        """
        client = OpenAISDK(api_key=self.token)
        embedding = client.embeddings.create(
            model=model,
            input=input
        )
        response = embedding.data[0].embedding

        return f"Created embedding using model {model} with input {input}. Response: {response}"
