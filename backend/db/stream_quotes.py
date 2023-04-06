import pathlib
import sys
from AlpacaStream.AlpacaDataStream import AlpacaDataStream
from models import Quotes
from helpers import insert_into_database
import pandas as pd
import logging

logger = logging.getLogger(__name__)

NY = 'America/New_York'

async def quotehandler(quotes):
    """
    Processes incoming quote data and saves it into the database.

    Args:
    quotes : Quotes object received from the Alpaca Data Stream API

    Returns:
    None
    """
    quotes_df = pd.DataFrame(quotes.__dict__)
    quotes_df = quotes_df.transpose()
    quotes_df['timestamp'] = pd.to_datetime(quotes_df['timestamp'], unit='ns')
    quotes_df.timestamp = quotes_df.timestamp.dt.tz_localize('UTC').dt.tz_convert(NY)
    quotes_df.rename(columns={"symbol": "ticker"}, inplace=True)
    insert_into_database(Quotes, quotes_df.to_dict(orient="records"))

def run_quotes_stream(tickers):
    """
    Runs the quotes streaming process for the specified tickers.

    Args:
    tickers : A list of ticker symbols for which the streaming process will be run.

    Returns:
    None
    """
    alpaca_obj = AlpacaDataStream()
    try:
        print("Streaming data for {} stocks".format(len(tickers)))
        alpaca_obj.get_streams("quotes", tickers, quotehandler)
        logger.info("Streaming quotes started")

    except Exception as e:
        logger.error("There was an error streaming quotes data. \n Error Details: {}".format(e))
        raise e

if __name__ == "__main__":
    symbols = ["AAPL", "MSFT"]
    run_quotes_stream(symbols)



    


