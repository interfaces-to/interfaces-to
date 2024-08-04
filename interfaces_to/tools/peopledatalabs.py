from typing import List, Dict, Any
from ..bases import FunctionSet
from ..utils import callable_function, tool_auth
from peopledatalabs import PDLPY

@tool_auth(token_env_name='PDL_API_KEY')
class PeopleDataLabs(FunctionSet):

    @callable_function
    def find_person(self, profile_url: str=None, email: str=None, linkedin_id: str=None, phone: str=None):
        """
        Get details about a person using their LinkedIn/Facebook/Twitter/GitHub/Instagram/Indeed url, email address, LinkedIn ID or phone number

        :param profile_url: The LinkedIn/Facebook/Twitter/GitHub/Instagram/Indeed url of the person e.g. https://linkedin.com/in/seanthorne
        :param email: The email address of the person e.g. renee.c.paulsen1959@yahoo.com
        :param linkedin_id: The LinkedIn ID of the person e.g. 145991517
        :param phone: The phone number of the person. For best results, use +[country code]. e.g. +1 555-234-1234
        """

        # check that at least one of the parameters is provided
        if not any([profile_url, email, linkedin_id, phone]):
            return "At least one of the parameters must be provided"

        client = PDLPY(api_key=self.token)

        # make a dict of the parameters that are not None
        params = {
            "profile": profile_url,
            "email": email,
            "lid": linkedin_id,
            "phone": phone
        }

        # remove the blank or None values from the params dict
        params = {k: v for k, v in params.items() if v}
        
        try:
            # get response by expanding params if the keys are not none
            response = client.person.enrichment(**params).json()

            return f"Response: {response}"
        except Exception as e:
            return f"Error: {e}"
    
    @callable_function
    def find_company(self, domain: str=None, company_name: str=None, ticker: str=None, profile_url: str=None):
        """
        Get details about a company using their domain, company name, ticker symbol or social media profile

        :param domain: The domain of the company e.g. google.com
        :param company_name: The name of the company e.g. Google, Inc.
        :param ticker: The stock ticker of the company e.g. GOOGL
        :param profile_url: The social profile url of the company e.g. linkedin.com/company/google
        """

        # check that at least one of the parameters is provided
        if not any([domain, company_name]):
            return "At least one of the parameters must be provided"

        client = PDLPY(api_key=self.token)

        # make a dict of the parameters that are not None
        params = {
            "website": domain,
            "name": company_name,
            "ticker": ticker,
            "profile": profile_url
        }

        # remove the blank or None values from the params dict
        params = {k: v for k, v in params.items() if v}
        
        try:
            # get response by expanding params if the keys are not none
            response = client.company.enrichment(**params).json()

            return f"Response: {response}"
        except Exception as e:
            return f"Error: {e}"