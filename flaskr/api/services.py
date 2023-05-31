import os
import requests
import pandas as pd
from flaskr import app
from retrying import retry
from flaskr import definitions as constants


class Serve3rdPartyAPI:
    """Class to handle third party api services"""

    ppp_data_path = None  # path for ppp data

    def __init__(self) -> None:
        """Constructor"""
        if not os.path.exists(constants.FETCHED_DATA_PATH):
            os.makedirs(constants.FETCHED_DATA_PATH)

        self.ppp_data_path = os.path.join(
            constants.FETCHED_DATA_PATH, constants.PPP_FILE_NAME
        )

    def _get_ppp_data(self):
        """Requests PPP data from Wold Bank API
        in JSON form
        """

        app.logger.info("Fetching the PPP data from World Bank API: Started")
        try:
            all_data = self._request_ppp_data()
            if all_data is None:
                app.logger.error("400 Bad Request: No ppp data recieved from api")
                return
        except Exception as e:
            app.logger.error(str(e))
            return

        app.logger.info("Data fetched successfully from World Bank API")

        # Getting parsed and filtered data
        parsed_df = self._parse_ppp_data(ppp_data=all_data)
        app.logger.info("Data parsed and filtered into a DataFrame")
        # Saving the data as csv in data dir
        self._save_ppp_data(parsed_ppp_data=parsed_df)

        app.logger.debug(
            "Top 10 data from the fetched PPP data = \n%s",
            parsed_df.head(10).to_string(index=False),
        )
        app.logger.info("PPP data fetched, parsed and saved in data directory")

    @retry(
        stop_max_attempt_number=constants.REQUEST_TRY_COUNT,  # Maximum number of retries
        wait_fixed=1000,  # Wait 1 second between retries
        retry_on_exception=lambda exc: isinstance(
            exc, requests.exceptions.RequestException
        ),  # Retry on network-related exceptions
    )
    def _request_ppp_data(self) -> list:
        """Requests the ppp data from world bank api endpoint

        Returns:
            list: list containing required data
        """
        app.logger.info("Started Requesting the data from World Bank API Endpoint")

        url = "https://api.worldbank.org/v2/country/all/indicator/PA.NUS.PPP"

        params = {
            "format": "json",
            "per_page": 10000,  # Number of records per page
            "date": "2019:2022",
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        all_data = data[1]

        return all_data if len(all_data) > 0 else None

    def _parse_ppp_data(self, ppp_data: list) -> pd.DataFrame:
        """Parse the fetched ppp data into a pandas dataframe after filtering it

        Args:
            ppp_data (list): List with ppp data in them

        Returns:
            pd.DataFrame: DataFrame containing parsed data as per requirement
        """
        records = []

        for record in ppp_data:
            country = record["country"]["value"]
            date = record["date"]
            value = record["value"]
            records.append([country, date, value])

        parsed_df = pd.DataFrame(records, columns=["Country", "Date", "Value"])
        parsed_df["Value"] = parsed_df["Value"].astype("float")
        parsed_df["Date"] = parsed_df["Date"].astype("int")

        # Discarding Nan data and keeping only one record for every country with most recent date/year
        filter1_df = parsed_df.loc[parsed_df["Value"].notna()]

        filter2_df = filter1_df.loc[
            filter1_df.groupby(by="Country")["Date"].idxmax()
        ].reset_index()

        return filter2_df

    def _save_ppp_data(self, parsed_ppp_data: pd.DataFrame) -> None:
        """Saves the parsed and filtered PPP data as csv in 'flaskr/data' directory

        Args:
            parsed_ppp_data (pd.DataFrame): PPP data after parsing and filtering
        """
        parsed_ppp_data.to_csv(
            os.path.join(
                constants.FETCHED_DATA_PATH,
                constants.PPP_FILE_NAME,
            ),
            sep="|",
            index=None,
        )

    def get_ppp_data(self):
        """Public method to call private method for ppp data 
        generation
        """
        self._get_ppp_data()


if __name__ == "__main__":
    Serve3rdPartyAPI().get_ppp_data()
