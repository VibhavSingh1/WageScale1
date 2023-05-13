import requests
import os
import json


class Serve3rdPartyAPI:
    """Class to handle third party api services"""

    def _get_ppp_data(self):
        """Requests PPP data from Wold Bank API
        in JSON form
        
        Keyword arguments:
        
        Return: json object
        """

        
        