import pathlib
import sys
import pandas as pd
import logging
from typing import List
from AlpacaStream.AlpacaDataStream import AlpacaDataStream
from models import Quotes, Stocks, BarHour, BarMinute, BarDaily, Trades
from helpers import insert_into_database

logger = logging.getLogger(__name__)
NY = 'America/New_York'


async def barhandler(bar):
    """
    A callback function to handle real-time bar data from Alpaca API.

    Args:
        bar: A bar object containing real-time bar data.

    Returns:
        None
    """
    # Convert bar data to pandas dataframe
    bar_df = pd.DataFrame(bar.__dict__)
    # Transpose the dataframe
    bar_df = bar_df.transpose()
    # Rename columns to match the database table
    bar_df.rename(columns={"symbol":"ticker"}, inplace=True)
    # Convert timestamp to datetime object and set timezone
    bar_df['timestamp'] = pd.to_datetime(bar_df['timestamp'],unit='ns')
    bar_df.timestamp = bar_df.timestamp.dt.tz_localize('UTC').dt.tz_convert(NY)
    # Insert data into the database
    insert_into_database(BarMinute, bar_df.to_dict(orient="records"))


def run_bar_stream(symbols: List[str]):
    """
    Function to stream real-time bar data from Alpaca API for a list of stock symbols.

    Args:
        symbols: A list of stock symbols to stream bar data for.

    Returns:
        None
    """
    # Create an instance of AlpacaDataStream class
    alpaca_obj = AlpacaDataStream()
    try:
        # Start streaming bar data for specified stock symbols
        logger.info("Streaming data for {} stocks".format(len(symbols)))
        alpaca_obj.get_streams("bars", symbols, barhandler)
        logger.info("Streaming bars started")

    except Exception as e:
        # Log any errors that occur during the streaming process
        logger.error("There was an error streaming bars data. Error details: {}".format(e))
        raise e


if __name__ == "__main__":
    # Example usage: stream real-time bar data for AAPL and MSFT stocks
    symbols = ["AAPL", "MSFT"]
    run_bar_stream(symbols)
