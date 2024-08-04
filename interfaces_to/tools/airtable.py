from typing import List, Dict, Any
from ..bases import FunctionSet
from ..utils import callable_function, tool_auth
import requests

@tool_auth(token_env_name='AIRTABLE_TOKEN')
class Airtable(FunctionSet):

    @callable_function
    def list_all_bases(self):
        """
        List all bases in your Airtable account
        """
        url = 'https://api.airtable.com/v0/meta/bases'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        bases = []
        offset = None

        while True:
            params = {}
            if offset:
                params['offset'] = offset

            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f'Error: {response.status_code}, {response.text}')
            
            data = response.json()
            bases.extend(data.get('bases', []))
            offset = data.get('offset')

            if not offset:
                break
        
        return bases
    
    @callable_function
    def get_base(self, base_id: str):
        """
        Get schema of the specified base in your Airtable account, including tables and views, and their fields
        
        :param base_id: The ID of the base to retrieve the schema for.
        """
        url = f'https://api.airtable.com/v0/meta/bases/{base_id}/tables'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Error: {response.status_code}, {response.text}')
        
        return response.json()

    @callable_function
    def list_base_records(self, base_id: str, table_id_or_name: str):
        """
        List records in a table in your Airtable account
        
        :param base_id: The ID of the base.
        :param table_id_or_name: The ID or name of the table.
        """
        url = f'https://api.airtable.com/v0/{base_id}/{table_id_or_name}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        records = []
        offset = None

        while True:
            params = {'pageSize': 100}
            if offset:
                params['offset'] = offset

            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f'Error: {response.status_code}, {response.text}')
            
            data = response.json()
            records.extend(data.get('records', []))
            offset = data.get('offset')

            if not offset:
                break

        return records
    
    @callable_function
    def create_base_records(self, base_id: str, table_id_or_name: str, records: List[Dict[str, Any]]):
        """
        Create records in a table in your Airtable account
        
        :param base_id: The ID of the base.
        :param table_id_or_name: The table ID or name of the table.
        :param records: A list of record objects to create.
        """
        url = f'https://api.airtable.com/v0/{base_id}/{table_id_or_name}'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'records': records
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return f'Error: {response.status_code}, {response.text}'
        
        return f"Response: {response.json()}"