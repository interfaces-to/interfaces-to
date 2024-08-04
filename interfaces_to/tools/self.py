import time
from typing import List
from ..bases import FunctionSet
from ..utils import callable_function


class Self(FunctionSet):

    @callable_function
    def wait(self, seconds : int):
        """
        Wait for a specified amount of time. Useful if you want to call another tool in the near future and need to wait for a response. Avoid waiting more than 30 seconds at a time and instead try the tool call before waiting again if necessary.
        
        :param seconds: The number of seconds to wait
        """
        time.sleep(seconds)
        return f"Waiting for {seconds} seconds"

    @callable_function
    def plan(self, steps : List[str], available_tools : List[str] = None):
        """
        If the user makes a complex request or you aren't sure what to do, make a plan by listing the steps you need to take. This is useful for breaking down a complex task into smaller, more manageable steps. Consider all available tools and resources when making your plan.

        :param steps: A list of steps to take
        :param available_tools: A list of tools that are available to help you complete
        """

        # build output 
        output = f"Plan: {steps}"
        if available_tools:
            output += f"\nAvailable tools: {available_tools}"
        return output
    
    @callable_function
    def get_time(self):
        """
        Get the current time
        """
        return time.ctime()
