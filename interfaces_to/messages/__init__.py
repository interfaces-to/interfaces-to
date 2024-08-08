import sys
from ..utils import LazyImport

message_listeners = [
    ('Slack', '.messages.slack', [('slack_sdk>=3.31.0')]),
    ('Ngrok', '.messages.ngrok', [('ngrok>=1.4.0')]),
    ('FastAPI', '.messages.fastapi', [('fastapi>=0.112.0'), ('uvicorn>=0.30.5')]),
    ('Gradio', '.messages.gradio', [('gradio>=4.40.0'), ('ipywidgets>=8.1.3')]),
    ('CLI', '.messages.cli', []),
]

for class_name, location, dependencies in message_listeners:
    sys.modules[__name__ + '.' + class_name] = LazyImport(location, class_name, dependencies)
    # create an attribute for each listener
    setattr(sys.modules[__name__], class_name, LazyImport(location, class_name, dependencies))

# only export what is needed
__all__ = [class_name for class_name, _, _ in message_listeners]
