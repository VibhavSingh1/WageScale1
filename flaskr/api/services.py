import io
import os
import pandas as pd
import requests
from retrying import retry

from flaskr import app
from flaskr import definitions as constants


class PPPData:
    """Class to handle third party PPP api services"""

    def __init__(self) -> None:
        """Constructor"""
        if not os.path.exists(constants.FETCHED_DATA_PATH):
            os.makedirs(constants.FETCHED_DATA_PATH)

        self.ppp_data_path = os.path.join(
            constants.FETCHED_DATA_PATH, constants.PPP_FILE_NAME
        )

    def _get_ppp_data(self) -> bool:
        """Requests PPP data from Wold Bank API
        in JSON form

        Returns:
            bool: True if the data has been saved or is present
        """

        app.logger.info("Fetching the PPP data from World Bank API: Started")
        try:
            all_data = self._request_ppp_data()
            if all_data is None:
                app.logger.error("400 Bad Request: No ppp data recieved from api")
                return False
        except Exception as e:
            app.logger.error(str(e))
            return False

        app.logger.info("Data fetched successfully from World Bank API")

        # Getting parsed and filtered data
        parsed_df = self._parse_ppp_data(ppp_data=all_data)
        parsed_df = parsed_df[["Country", "Date", "Value"]]
        app.logger.info("Data parsed and filtered into a DataFrame")

        # Saving the data as csv in data dir
        self._save_ppp_data(parsed_ppp_data=parsed_df)

        app.logger.debug(
            "Top 10 data from the fetched PPP data = \n%s",
            parsed_df.head(10).to_string(index=False),
        )
        app.logger.info("PPP data fetched, parsed and saved in data directory")

        return True

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
            self.ppp_data_path,
            sep="|",
            index=False,
        )
    
    def _check_available_data(self) -> bool:
        """Check if there is data file is available or not

        Returns:
            bool: True if available else False
        """
        check_result = os.path.exists(self.ppp_data_path)
        return check_result

    def get_ppp_data(self) -> bool:
        """Public method to call private method for ppp data
        generation

        Returns:
            bool: True if the task is successful else False
        """
        flag = self._get_ppp_data()
        if flag is False:
            return self._check_available_data()
        else:
            return True


class ExchangeRateData:
    """Class to handle third party Exchange Rates api services : Monthly calls limit is 1000"""

    def __init__(self) -> None:
        """Constructor"""
        if not os.path.exists(constants.FETCHED_DATA_PATH):
            os.makedirs(constants.FETCHED_DATA_PATH)

        self.exch_rate_data_path = os.path.join(
            constants.FETCHED_DATA_PATH, constants.EXCH_RATE_FILE_NAME
        )

    def _get_exch_rate_data(self) -> bool:
        """Generates the exchange rate data after fetching from openexchangerates.org
        in JSON form

        Returns:
            bool: True if data generated successfully else False
        """
        app.logger.info("Fetching the Echange Rate data from openexchangerates.org: Started")
        try:
            response = self._request_exch_rate_data()
        except Exception as e:
            app.logger.error(str(e))
            return False

        app.logger.info("Data fetched successfully from openexchangerates.org")

        # Getting parsed and filtered data
        all_data = response.json()
        parsed_df = self._parse_exch_rate_data(exch_rate_data=all_data)
        app.logger.info("Data parsed and filtered into a DataFrame")

        # Saving the data as csv in data dir
        self._save_exch_rate_data(parsed_exch_rate_data=parsed_df)
        app.logger.debug(
            "Top 10 data from the fetched exchange rate data = \n%s",
            parsed_df.head(10).to_string(index=False),
        )
        app.logger.info(
            "Exchange Rate data fetched, parsed and saved in data directory"
        )

        return True

    @retry(
        stop_max_attempt_number=constants.REQUEST_TRY_COUNT,  # Maximum number of retries
        wait_fixed=1000,  # Wait 1 second between retries
        retry_on_exception=lambda exc: isinstance(
            exc, requests.exceptions.RequestException
        ),  # Retry on network-related exceptions
    )
    def _request_exch_rate_data(self) -> requests.Response:
        """Requests the exchange rate data from openexchangerates.org api endpoint

        Returns:
            list: list containing required data
        """
        app.logger.info("Started Requesting the data from World Bank API Endpoint")

        url = "https://openexchangerates.org/api/latest.json"
        params = {
            "base": "USD",
            "app_id": "d0f60989add94a08a9aa685f1f2a9d34",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response

    def _parse_exch_rate_data(self, exch_rate_data: list) -> pd.DataFrame:
        """Parse the fetched exchange rate data into a pandas dataframe after filtering it

        Args:
            exch_rate_data (list): List with exchange rate data in them

        Returns:
            pd.DataFrame: DataFrame containing parsed data as per requirement
        """
        exch_rate_df = pd.DataFrame(
            data=[*exch_rate_data["rates"].items()],
            columns=["AlphabeticCode", "ExchangeRate"],
        )

        return exch_rate_df

    def _save_exch_rate_data(self, parsed_exch_rate_data: pd.DataFrame) -> None:
        """Saves the parsed and filtered data as csv in 'flaskr/data' directory

        Args:
            parsed_exch_rate_data (pd.DataFrame): PPP data after parsing and filtering
        """
        parsed_exch_rate_data.to_csv(
            self.exch_rate_data_path,
            sep="|",
            index=False,
        )
    
    def _check_available_data(self) -> bool:
        """Check if there is data file is available or not

        Returns:
            bool: True if available else False
        """
        check_result = os.path.exists(self.exch_rate_data_path)

        return check_result


    def get_exch_rate_data(self):
        """Public method to call private method for exchange rate data
        generation
        """
        flag = self._get_exch_rate_data()
        if flag is False:
            return self._check_available_data()
        else:
            return True


class CurrencyData:
    """Class to handle [Country, Currency] data fetching"""

    def __init__(self) -> None:
        """Constructor initializing instance level variables"""

        if not os.path.exists(constants.FETCHED_DATA_PATH):
            os.makedirs(constants.FETCHED_DATA_PATH)

        self.data_file_path = os.path.join(
            constants.FETCHED_DATA_PATH,
            constants.CURRENCY_FILE_NAME,
        )

    def _get_currency_data(self) -> bool:
        """Request data from the URL, parse it and save it at
        "flaskr/data/fetched" if doesn't exist

        Returns:
            bool: True if file fetched or exists
                    False if file doesn't exist and failed to fetch a new
        """
        # Check if file exists; if yes then return True
        if self._check_available_data():
            app.logger.info("Currency data already exists, skipping the fetching")
            return True

        # File doesn't exist, so fetch a new
        app.logger.info("Fetching the Currencies data: Started")
        try:
            response = self._request_currency_data()

        except Exception as e:
            app.logger.error(str(e))
            return False

        app.logger.info("Data fetched successfully")

        # Parsing the data fetched
        data = response.content
        parsed_df = self._parse_data(data=data)
        parsed_df = parsed_df[['Entity', 'Currency', 'AlphabeticCode']]
        app.logger.info(
            "Parsed the fetched data into dataframe with %s records", parsed_df.shape[0]
        )

        self._save_currency_data(dataframe=parsed_df)
        app.logger.info(
            "Currency data fetched, parsed and saved at %s", self.data_file_path
        )
        app.logger.debug(
            "Top 10 data final currency data = \n%s",
            parsed_df.head(10).to_string(index=False),
        )

        return True

    @retry(
        stop_max_attempt_number=constants.REQUEST_TRY_COUNT,  # Maximum number of retries
        wait_fixed=1000,  # Wait 1 second between retries
        retry_on_exception=lambda exc: isinstance(
            exc, requests.exceptions.RequestException
        ),  # Retry on network-related exceptions
    )
    def _request_currency_data(self) -> requests.Response:
        """Requests the new file from url and returns a response object

        Returns:
            requests.Response: Response returned from the request of get data
        """

        url = "https://datahub.io/core/currency-codes/r/0.csv"

        response = requests.get(url=url)
        response.raise_for_status()

        return response

    def _parse_data(self, data: bytes) -> pd.DataFrame:
        """Parse the data fetched into tabular form as dataframe

        Args:
            data (bytes): data downloaded from the URL

        Returns:
            pd.DataFrame: Downloaded data parsed into a dataframe
        """

        data_frame = pd.read_csv(io.BytesIO(data))

        return data_frame

    def _save_currency_data(self, dataframe: pd.DataFrame):
        """Saves the currency dataset as csv in data dir

        Args:
            dataframe (pd.DataFrame): dataframe containing the currency data
        """

        dataframe.to_csv(
            self.data_file_path,
            sep="|",
            index=False,
        )

    def _check_available_data(self) -> bool:
        """Check if there is data file is available or not

        Returns:
            bool: True if available else False
        """
        check_result = os.path.exists(self.data_file_path)

        return check_result


    def get_currency_data(self) -> bool:
        """Public Method to call private methods

        Returns:
            bool: If successful then returns True else False
        """
        flag = self._get_currency_data()
        return flag

class GenerateData:
    """class to handle data generation from the fetched data
    """
    def __init__(self) -> None:
        if not os.path.exists(constants.GENERATED_DATA_PATH):
            os.makedirsO(constants.GENERATED_DATA_PATH)
        
        self.final_merged_data_file_path = os.path.join(
            constants.GENERATED_DATA_PATH,
            constants.FINAL_MERGED_DATA_FILE,
        )

        self.currency_file_path = os.path.join(
            constants.FETCHED_DATA_PATH,
            constants.CURRENCY_FILE_NAME,
        )

        self.ppp_file_path = os.path.join(
            constants.FETCHED_DATA_PATH,
            constants.PPP_FILE_NAME,
        )

        self.exch_rate_file_path = os.path.join(
            constants.FETCHED_DATA_PATH,
            constants.EXCH_RATE_FILE_NAME,
        )
    
    def _generate_merged_final_data(self) -> bool:
        """Reads fetched data (if all available) and generate the required 
        final dataframe from the data

        Returns:
            bool: True if final merged data generated successfully, else False
        """

        # Check if the required fetched files exist
        exist = self._check_if_files_exist()
        if not exist:
            app.logger.error("Required Data is unavailable for application to use!!")
            return False
        
        # Data is available - Proceeding with final data generation
        currency_file_df = pd.read_csv(
            self.currency_file_path,
            sep="|",
        )
        ppp_file_df = pd.read_csv(
            self.ppp_file_path,
            sep="|",
        )

        exch_rate_file_df = pd.read_csv(
            self.exch_rate_file_path,
            sep="|",
        )

        # Getting ["Country", "AlphabeticCode", "Value"] columns
        merge1 = pd.merge(
            left=ppp_file_df,
            left_on="Country",
            right=currency_file_df,
            right_on="Entity",
            how="inner",
        )
        merge1 = merge1[["Country", "AlphabeticCode", "Value"]]
        app.logger.debug("Top 10 data after first merge [ppp and currency data] =\n%s",
                         merge1.head(10).to_string(index=False)
                         )

        # Getting ["Country", "AlphabeticCode", "Value", "ExchangeRate"] columns
        merge2 = pd.merge(
            left=merge1,
            right=exch_rate_file_df,
            on="AlphabeticCode",
            how="inner",
        )

        merge2.sort_values(by=["Country"])
        app.logger.debug("Top 10 data after second merge [merged1 and exchange rate data] =\n%s",
                         merge2.head(10).to_string(index=False)
                         )
        app.logger.info("Final merged data generation complete")        

    def _check_if_files_exist(self) -> bool:
        """Checks if all the files for merged file generation, exist

        Returns:
            bool: True if all exist, False if any or all are missing
        """
        curr_file_exists = os.path.exists(self.currency_file_path)
        ppp_file_exists = os.path.exists(self.ppp_file_path)
        exch_rate_file_exists = os.path.exists(self.exch_rate_file_path)

        if exch_rate_file_exists and ppp_file_exists and curr_file_exists:
            return True
        else:
            return False


if __name__ == "__main__":
    PPPData().get_ppp_data()
