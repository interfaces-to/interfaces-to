from typing import List
from ..bases import FunctionSet
from ..utils import callable_function

class System(FunctionSet):

    @callable_function
    def get_system_message(self):
        """
        Read your system message (system prompt). The system message provides your instructions that define how you should interact with users.
        
        """
        return f"System message is {self.system.get('content')}" if self.system else "No system message available"

    @callable_function
    def set_system_message(self, message: str):
        """
        Set your system message (system prompt). The system message provides your instructions that define how you should interact with users. Always use instruction format. e.g. "You are a helpful assistant."
        
        :param message: The message to set as the system message in the form of instructions. e.g. "You are a helpful assistant."
        """
        self.system = {"role":"system","content": message}
        return f"System message set to {message}"
    
    @callable_function
    def clear_system_message(self):
        """
        Clear your system message (system prompt). The system message provides your instructions that define how you should interact with users.
        
        """
        self.system = None
        return "System message cleared"
