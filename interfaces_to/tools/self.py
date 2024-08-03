import time
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
