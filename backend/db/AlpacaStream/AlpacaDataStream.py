import asyncio
import sys
import pathlib
import os
import time
from typing import List
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
import logging

load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

class AlpacaDataStream:
    """
    Class for managing the Alpaca data stream.
    """

    def __init__(self):
        """
        Constructor for the AlpacaDataStream class.
        """
        self._conn = None
        self.create_connection()

    def get_market_clock(self):
        """
        Retrieves the market clock from Alpaca.

        Returns:
            clk (dict): A dictionary containing the market clock information.
        """
        try:
            obj = REST()
            clk = obj.get_clock()
            return clk
        except Exception as e:
            return ConnectionError

    def create_connection(self):
        """
        Creates a connection to the Alpaca data stream.
        """
        try:
            self._conn = Stream(os.environ["APCA_API_KEY_ID"], os.environ["APCA_API_SECRET_KEY"], base_url=os.environ["APCA_API_BASE_URL"], data_feed=os.environ["APCA_FEED"])
        except Exception as e:
            raise ConnectionError("Some error in streaming data /n {}".format(e))

    def get_streams(self, channel: str, symbols: List[str], handlers: List[callable]):
        """
        Subscribes to data streams for the given channel, symbols, and handlers.

        Args:
            channel (str): The data stream channel to subscribe to. Can be "bars", "trades", or "quotes".
            symbols (List[str]): A list of symbols to subscribe to.
            handlers (List[callable]): A list of callable objects that will handle the incoming data stream.

        Raises:
            Exception: An exception is raised if there is an error connecting to the server.
        """
        if channel == "bars":
            self._conn.subscribe_bars(handlers, *symbols)
        elif channel == "trades":
            self._conn.subscribe_trade_updates(handlers)
            self._conn.subscribe_trades(handlers, *symbols)
        elif channel == "quotes":
            self._conn.subscribe_quotes(handlers, *symbols)

        try:
            logger.info("Connecting to Alpaca server")
            self._conn.run()
            logger.info("Connection to Alpaca server terminated")
            print("Connection established with Alpaca server")
        except Exception as e:
            logger.exception("Some error connecting to server. Check logs.")
            raise e
        finally:
            print("Trying to re-establish connection")
            time.sleep(5)
            res = self._conn.run()
