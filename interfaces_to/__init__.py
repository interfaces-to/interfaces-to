from dotenv import load_dotenv
load_dotenv()

import sys
from .utils import LazyImport, run, running, import_tools, read_messages

# all tools are imported lazily to avoid hard package dependencies
tool_classes = [
    ('Self', '.tools.self'),
    ('Slack', '.tools.slack'),
    ('OpenAI', '.tools.openai'),
    ('Notion', '.tools.notion'),
    ('Airtable', '.tools.airtable'),
    ('PeopleDataLabs', '.tools.peopledatalabs')
]

# create a module for each tool
for class_name, location in tool_classes:
    sys.modules[__name__ + '.' + class_name] = LazyImport(location, class_name)
    
    # create an attribute for each tool
    setattr(sys.modules[__name__], class_name, LazyImport(location, class_name))

# only export what is needed
__all__ = [class_name for class_name, _  in tool_classes] + [run, running, import_tools, read_messages]

