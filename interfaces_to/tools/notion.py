from ..bases import FunctionSet
from ..utils import callable_function, tool_auth
from notion_client import Client, APIErrorCode, APIResponseError

@tool_auth(token_env_name='NOTION_TOKEN')
class Notion(FunctionSet):

    @callable_function
    def list_notion(self, title=""):
        """
        List all pages and databases in Notion and optionally filter by title
        
        :param title: A string to filter the results by title
        """
        notion = Client(auth=self.token)

        try:
            response = notion.search(query=title)

            return f"Listing everything in Notion{(', filtered by: ' + title) if title != '' else ''}. Response: {response}"
        except APIResponseError as e:
            return f"Error: {e}"

    @callable_function
    def query_notion_database(self, database_id: str):
        """
        Query a database in Notion
        
        :param database_id: The ID of the database to query. To get a database ID, use the list_notion function.
        """
        notion = Client(auth=self.token)
        try:
            response = notion.databases.query(database_id=database_id)

            return f"Querying database {database_id} in Notion. Response: {response}"
        except APIResponseError as e:
            return f"Error: {e}"

    @callable_function
    def create_notion_page(self, parent_id: dict, children: dict = {}, properties: dict = {}):
        """
        Create a page in Notion
        
        :param parent_id: The ID of the parent page to create the new page under.
        :param children: The array of block objects of the new page
        :param properties: The properties of the new page
        """
        notion = Client(auth=self.token)

        try:
            created_page = notion.pages.create(
                parent=parent_id, children=children, properties=properties)

            return f"Creating page in Notion under {parent_id}. Response: {created_page}"
        except APIResponseError as e:
            return f"Error: {e}"

    @callable_function
    def read_notion_page(self, page_id: str):
        """
        Read the contents of a page in Notion
        
        :param page_id: The ID of the page to read.
        """
        notion = Client(auth=self.token)
        try:
            response = notion.pages.retrieve(page_id=page_id)

            return f"Reading page {page_id} in Notion. Response: {response}"
        except APIResponseError as e:
            return f"Error: {e}"
