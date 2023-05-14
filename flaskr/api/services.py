import requests
import pandas as pd
import json


class Serve3rdPartyAPI:
    """Class to handle third party api services"""

    def _get_ppp_data(self):
        """Requests PPP data from Wold Bank API
        in JSON form

        Return: json object
        """

        response = requests.get(
            url="https://api.worldbank.org/v2/country/all/indicator/PA.NUS.PPP?format=JSON",
            timeout=5,
        )

        if response.status_code == 200:
            data_json = response.json()

            data = data_json[1] 

            # Create a DataFrame from the data
            df = pd.DataFrame(data)

            df = df[['country', 'date', 'value']]
            df.columns = ['Country', 'Date', 'Value']

            # Print the DataFrame
            print(df.head(1).values)


        else:
            print(response.status_code)



if __name__ == "__main__":

    Serve3rdPartyAPI()._get_ppp_data()
