import pathlib
import sys
from AlpacaStream.AlpacaDataStream import AlpacaDataStream
from models import Quotes, Stocks, BarHour, BarMinute, BarDaily, Trades
from helpers import insert_into_database
import pandas as pd
import logging

logger = logging.getLogger("__name__")
NY = 'America/New_York'

async def tradehandler(trades):
    """
    Processes trade data received through AlpacaDataStream API and saves it to a database using helper functions.

    Args:
        trades: A trade object received from AlpacaDataStream API.

    Returns:
        None.
    """
    print(trades.__dict__)
    trades_df = pd.DataFrame(trades.__dict__)
    trades_df = trades_df.transpose()
    trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'], unit='ns')
    trades_df.timestamp = trades_df.timestamp.dt.tz_localize('UTC').dt.tz_convert(NY)
    trades_df.rename(columns={"symbol":"ticker","id":"trade_id"}, inplace=True)
    insert_into_database(Trades, trades_df.to_dict(orient="records"))

def run_trades_stream(tickers):
    """
    Initiates a stream of trade data using AlpacaDataStream API and processes the received data using the tradehandler() function.

    Args:
        tickers: A list of ticker symbols for which to receive trade data.

    Returns:
        None.
    """
    alpaca_obj = AlpacaDataStream()
    try:
        print("streaming data for {} stocks".format(len(tickers)))
        alpaca_obj.get_streams("trades", tickers, tradehandler)
        logger.info("streaming trades started")
    except Exception as e:
        logger.error("there was some error streaming trades data \n Error Details:{}".format(e))
        raise e

if __name__ == "__main__":
    symbols = ["AAPL", "MSFT"]
    run_trades_stream(symbols)



    


