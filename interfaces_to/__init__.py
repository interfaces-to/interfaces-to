from dotenv import load_dotenv
load_dotenv()

import sys
from .utils import run, running, tools, LazyImport

# all tools are imported lazily to avoid hard package dependencies
tool_classes = [
    ('Slack', '.tools.slack', 'Slack'),
    ('OpenAI', '.tools.openai', 'OpenAITool'),
    ('Notion', '.tools.notion', 'Notion'),
    ('Self', '.tools.self', 'Self'),
]

# create a module for each tool
for name, location, class_name in tool_classes:
    sys.modules[__name__ + '.' + name] = LazyImport(location, class_name)

# only export what is needed
__all__ = [class_name for _, _, class_name in tool_classes] + ['tools', 'run', 'running']
