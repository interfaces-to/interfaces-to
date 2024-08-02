from ..bases import FunctionSet, JSONSerializableFunction
import os
from notion_client import Client, APIErrorCode, APIResponseError


class Notion(FunctionSet):

    class List(JSONSerializableFunction):
        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "list_notion",
                "description": "List all pages and databases in Notion and optionally filter by title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "A string to filter the results by title",
                        },
                    },
                    "required": [],
                },
            }

        def list_notion(self, title=""):

            notion = Client(auth=os.environ["NOTION_TOKEN"])

            try:
                response = notion.search(query=title)

                return f"Listing everything in Notion{(', filtered by: ' + title) if title != '' else ''}. Response: {response}"
            except APIResponseError as e:
                return f"Error: {e}"

    class DatabaseQuery(JSONSerializableFunction):
        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "query_notion_database",
                "description": "Query a database in Notion",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "database_id": {
                            "type": "string",
                            "description": "The ID of the database to query. To get a database ID, use the list_notion function.",
                        }
                    },
                    "required": ["database_id"],
                },
            }

        def query_notion_database(self, database_id):
            notion = Client(auth=os.environ["NOTION_TOKEN"])
            try:

                response = notion.databases.query(database_id=database_id)

                return f"Querying database {database_id} in Notion. Response: {response}"

            except APIResponseError as e:
                return f"Error: {e}"

    class CreatePage(JSONSerializableFunction):
        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "create_notion_page",
                "description": "Create a page in Notion",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_id": {
                            "type": "object",
                            "description": "The ID of the parent page to create the new page under.",
                            "properties": {
                                "database_id": {
                                    "type": "string",
                                    "description": "The ID of the database to create the page under",
                                },
                            }

                        },
                        "children": {
                            "type": "array",
                            "description": "The array of block objects of the new page",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "object": {
                                        "type": "string",
                                        "description": "The type of block object. e.g. \"block\" or \"page\"",
                                    },
                                    "type": {
                                        "type": "string",
                                        "description": "The type of block. e.g. \"heading_1\" or \"paragraph\"",
                                    },
                                    "paragraph": {
                                        "type": "object",
                                        "description": "The paragraph content of the block",
                                        "properties": {
                                            "rich_text": {
                                                "type": "array",
                                                "description": "The rich text content of the paragraph",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "type": {
                                                            "type": "string",
                                                            "description": "The type of content. e.g. \"text\" or \"mention\"",
                                                        },
                                                        "text": {
                                                            "type": "object",
                                                            "description": "The text content",
                                                            "properties": {
                                                                "content": {
                                                                    "type": "string",
                                                                    "description": "The actual text content",
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "properties": {
                            "type": "object",
                            "description": "The properties of the new page",

                            "properties": {
                                "title": {
                                    "type": "object",
                                    "description": "The title of the new page",
                                },
                            },

                        },
                    },
                    "required": ["parent_id", "children", "properties"],
                },
            }

        def create_notion_page(self, parent_id, children={}, properties={}):

            notion = Client(auth=os.environ["NOTION_TOKEN"])

            try:
                created_page = notion.pages.create(
                    parent=parent_id, children=children, properties=properties)

                return f"Creating page in Notion under {parent_id}. Response: {created_page}"
            except APIResponseError as e:
                return f"Error: {e}"
    
    class ReadPage(JSONSerializableFunction):
        def __init__(self, tool):
            super().__init__(tool)
            self['type'] = "function"
            self['function'] = {
                "name": "read_notion_page",
                "description": "Read the contents of a page in Notion",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page to read.",
                        }
                    },
                    "required": ["page_id"],
                },
            }

        def read_notion_page(self, page_id):
            notion = Client(auth=os.environ["NOTION_TOKEN"])
            try:
                response = notion.pages.retrieve(page_id=page_id)

                return f"Reading page {page_id} in Notion. Response: {response}"
            except APIResponseError as e:
                return f"Error: {e}"

    def __init__(self, token=None, functions=None):
        self.token = token

        # try and load token from os.environ["NOTION_TOKEN"]
        if token is None:
            try:
                self.token = os.environ["NOTION_TOKEN"]
            except KeyError:
                raise ValueError(
                    "No token provided and NOTION_TOKEN not found in environment variables")

        # create a manual mapping of function names to classes
        self.functions_map = {
            'search_notion': self.List,
            'query_notion_database': self.DatabaseQuery,
            'create_notion_page': self.CreatePage,
            'read_notion_page': self.ReadPage,
        }

        if functions is None:
            functions = self.functions_map.keys()

        # instantiate each class and add it to the class instance for the functions in the constructor
        self.functions = [self.functions_map[function]
                          (self) for function in functions]
