import sys

from ..utils import LazyImport

message_listeners = [
    ('Slack', '.messages.slack')
]

for class_name, location in message_listeners:
    sys.modules[__name__ + '.' + class_name] = LazyImport(location, class_name)

    # create an attribute for each listener
    setattr(sys.modules[__name__], class_name, LazyImport(location, class_name))

# only export what is needed
__all__ = [class_name for class_name, _ in message_listeners]