import time
from typing import List
from ..bases import FunctionSet
from ..utils import callable_function
import ast, operator, math

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
    
    @callable_function
    def do_math(self, expression: str):
        """
        Perform a mathematical operation and return the result. Useful for evaluating mathematical expressions reliably.

        Supported operators: +, -, *, /, **, %, ^, unary - 
        Supported constants: pi (π), e, tau (τ), inf, nan
        Supported functions: sin(x), cos(x), tan(x), log(x), log10(x), sqrt(x), exp(x), 
        pow(x, y), fabs(x), factorial(x), gcd(x, y), degrees(x), radians(x), sinh(x), 
        cosh(x), tanh(x), asin(x), acos(x), atan(x), atan2(y, x), ceil(x), floor(x), 
        trunc(x), isfinite(x), isinf(x), isnan(x)

        :param expression: The mathematical expression to evaluate, e.g. 
        "sin(pi / 4) + log10(1000) - sqrt(49) * pow(2, 3) / fabs(-10.5) + factorial(5) - 
        gcd(48, 18) + tanh(1) + atan2(1, 1)"
        """
        def eval_expr(expr):
            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.BitXor: operator.xor,
                ast.USub: operator.neg,
            }

            functions = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'exp': math.exp,
                'pow': math.pow,
                'fabs': math.fabs,
                'factorial': math.factorial,
                'gcd': math.gcd,
                'degrees': math.degrees,
                'radians': math.radians,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'atan2': math.atan2,
                'ceil': math.ceil,
                'floor': math.floor,
                'trunc': math.trunc,
                'isfinite': math.isfinite,
                'isinf': math.isinf,
                'isnan': math.isnan,
            }

            constants = {
                'pi': math.pi,
                'e': math.e,
                'tau': math.tau,
                'inf': math.inf,
                'nan': math.nan,
            }

            def _eval(node):
                if isinstance(node, ast.BinOp):
                    left = _eval(node.left)
                    right = _eval(node.right)
                    return operators[type(node.op)](left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = _eval(node.operand)
                    return operators[type(node.op)](operand)
                elif isinstance(node, ast.Call):
                    func_name = node.func.id
                    if func_name in functions:
                        args = [_eval(arg) for arg in node.args]
                        return functions[func_name](*args)
                    else:
                        return f"Unsupported function: {func_name}"
                elif isinstance(node, ast.Name):
                    if node.id in constants:
                        return constants[node.id]
                    else:
                        return f"Unknown variable or constant: {node.id}"
                elif isinstance(node, (ast.Num, ast.Constant)):
                    return node.n if hasattr(node, 'n') else node.value
                else:
                    return f"Unsupported AST node type: {type(node).__name__}"

            try:
                node = ast.parse(expr, mode='eval')
                return _eval(node.body)
            except Exception as e:
                return f"Error: {e}"

        result = eval_expr(expression)
        return f"Result: {result}"