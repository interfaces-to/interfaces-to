from dotenv import load_dotenv
load_dotenv()

import sys
from .utils import LazyImport, run, running, import_tools, read_messages
from .agent import Agent

# all tools are imported lazily to avoid hard package dependencies
tool_classes = [
    ('Self', '.tools.self', []),
    ('System', '.tools.system', []),
    ('Slack', '.tools.slack', [('slack_sdk>=3.31.0')]),
    ('OpenAI', '.tools.openai', [('openai>=1.37.1')]),
    ('Notion', '.tools.notion', [('notion-client>=2.2.1')]),
    ('Airtable', '.tools.airtable', []),
    ('PeopleDataLabs', '.tools.peopledatalabs', [('peopledatalabs>=4.0.0')]),
]

# create a module for each tool
for class_name, location, dependencies in tool_classes:
    sys.modules[__name__ + '.' + class_name] = LazyImport(location, class_name, dependencies)
    
    # create an attribute for each tool
    setattr(sys.modules[__name__], class_name, LazyImport(location, class_name, dependencies))

# only export what is needed
__all__ = [class_name for class_name, _, _  in tool_classes] + [run, running, import_tools, read_messages, Agent]

