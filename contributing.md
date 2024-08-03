# Contributors Guide

This document is a guide for contributors to `into`. It outlines the process for contributing to the project, as well as the standards and conventions that contributors are expected to follow.

These are the core development principles that the project follows:

1. **Let the LLM do the work:** We always prefer to solve problems by providing tools that allow the LLM to do the work, rather than by adding heurestics or wrappers to the LLM execution itself. Up to 128 tools can be provided during execution (the current OpenAI API limitation), which provides plenty of options for the LLM to combine tools to address a prompt. With `parallel_tool_calls` enabled (which it is), the combinatoric potential of these tools is even greater.
   
2. **Keep it beginner-friendly:** We want to make it as easy as possible for builders of all skill levels to use `into` in their LLM-enabled projects. This means minimising boilerplate requirements, keeping Python tricks behind the scenes, avoiding complex dependencies and providing clear and concise documentation with plenty of examples.

3. **Make more tools:** The best way to improve `into` is to add more tools. If you have an idea for a tool that would be useful for the LLM, please consider contributing it to the project. We are always looking for new tools to add to the library. Tools should always rely on web service APIs and include the minimum necessary authentication and configuration. Tools should be well-documented and tested before being submitted for review.
   
4. **Minimal function design:** Tools can include many functions, but that does not mean they should. Functions should be designed to be as simple and easy to use as possible, which might mean combining multiple API calls into a single tool, to avoid multiple function calls in the LLM.

5. **Be secure:** Tools should never allow for the execution of arbitrary code in unsandboxed environments. Tools should always be designed to be safe to use in a production environment. Tools should be reviewed by the community before being merged into the project.

## Creating a new tool

Please be aware that the `into` project is still in its early stages, and the process for contributing a new tool is still being developed with regular breaking changes to the API. If you are interested in contributing a new tool, please reach out to the project maintainers for guidance.

Tools can be added by creating a new Python file in the `interfaces_to/tools` directory and adding the tool to the `tool_classes` definition in `interfaces_to/__init__.py`.

A tool should be a single class that inherits from `FunctionSet`. The class should include the functions that the tool provides for calling, decorated with the `@callable_function` decorator. Each function should include a docstring that describes the function and its parameters, and the function should define type hints for its parameters. An error will be raised if the decorated fuction does not implement these things. Any parameters without a default value will be treated as required parameters, and any parameters with a default value will be treated as optional parameters.