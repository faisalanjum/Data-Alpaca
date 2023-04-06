from enum import Enum
import time
import alpaca_trade_api as tradeapi
import asyncio
from dotenv import load_dotenv
import os
import pandas as pd
import sys
from alpaca_trade_api.rest import TimeFrame, URL
from alpaca_trade_api.rest_async import gather_with_concurrency, AsyncRest

load_dotenv()

NY = 'America/New_York'
api_key_id = os.environ.get('APCA_API_KEY_ID')
api_secret = os.environ.get('APCA_API_SECRET_KEY')
base_url = os.environ.get('APCA_API_BASE_URL')
feed = os.environ.get('APCA_FEED')
rest = AsyncRest(key_id=api_key_id, secret_key=api_secret)
api = tradeapi.REST(key_id=api_key_id, secret_key=api_secret, base_url=URL(base_url))


class DataType(str, Enum):
    Bars = "Bars"
    Trades = "Trades"
    Quotes = "Quotes"


def get_data_method(data_type: DataType):
    """
    Returns the corresponding async data retrieval method for the given data type.

    Args:
        data_type (DataType): The type of data to retrieve.

    Returns:
        function: The corresponding async data retrieval method for the given data type.

    Raises:
        Exception: If an unsupported data type is provided.
    """
    if data_type == DataType.Bars:
        return rest.get_bars_async
    elif data_type == DataType.Trades:
        return rest.get_trades_async
    elif data_type == DataType.Quotes:
        return rest.get_quotes_async
    else:
        raise Exception(f"Unsupported data type: {data_type}")


async def get_historic_data_base(symbols, data_type: DataType, start, end,
                                 timeframe: TimeFrame = None):
    """
    Base function to retrieve historic data for a given set of symbols and time range.

    Args:
        symbols (list): List of symbols to retrieve data for.
        data_type (DataType): The type of data to retrieve.
        start (str): The start date of the data range to retrieve in 'YYYY-MM-DD' format.
        end (str): The end date of the data range to retrieve in 'YYYY-MM-DD' format.
        timeframe (TimeFrame, optional): The timeframe of the data to retrieve. Defaults to None.

    Returns:
        list: A list of tuples containing the retrieved data.

    Raises:
        Exception: If the python version is lower than 3.6 or if an error occurs during data retrieval.
    """
    major = sys.version_info.major
    minor = sys.version_info.minor
    if major < 3 or minor < 6:
        raise Exception('asyncio is not support in your python version')
    msg = f"Getting {data_type} data for {len(symbols)} symbols"
    msg += f", timeframe: {timeframe}" if timeframe else ""
    msg += f" between dates: start={start}, end={end}"
    print(msg)
    step_size = 1
    results = []
    for i in range(0, len(symbols), step_size):
        tasks = []
        for symbol in symbols[i:i+step_size]:
            args = [symbol, start, end, timeframe.value] if timeframe else \
                [symbol, start, end]
            tasks.append(get_data_method(data_type)(*args))

        if minor >= 8:
            results.extend(await asyncio.gather(*tasks, return_exceptions=False))
        else:
            results.extend(await gather_with_concurrency(500, *tasks))

    bad_requests = 0

    for response in results:
        if isinstance(response, Exception):
            print(f"Got an error: {response}")
        elif not len(response[1]):
            bad_requests += 1

    print(f"Total of {len(results)} {data_type}, and {bad_requests} "
          f"empty responses.")

    return results




async def get_historic_bars(symbols, start, end, timeframe: TimeFrame):
    data=await get_historic_data_base(symbols, DataType.Bars, start, end, timeframe)
    return data

async def get_historic_trades(symbols, start, end, timeframe: TimeFrame):
    """
    Asynchronously retrieves historical trades data for a given symbol, timeframe, and time range.

    Args:
        symbols (list): A list of symbols to retrieve historical data for.
        start (str): The start date of the historical data range in the format YYYY-MM-DD.
        end (str): The end date of the historical data range in the format YYYY-MM-DD.
        timeframe (TimeFrame): The timeframe of the historical trades data.

    Returns:
        data (dict): A dictionary containing the historical trades data for the specified symbols, timeframe, and time range.
    """
    data=await get_historic_data_base(symbols, DataType.Trades, start, end)
    return data


async def get_historic_quotes(symbols, start, end, timeframe: TimeFrame):
    """
    Asynchronously retrieves historical quotes data for a given symbol, timeframe, and time range.

    Args:
        symbols (list): A list of symbols to retrieve historical data for.
        start (str): The start date of the historical data range in the format YYYY-MM-DD.
        end (str): The end date of the historical data range in the format YYYY-MM-DD.
        timeframe (TimeFrame): The timeframe of the historical quotes data.

    Returns:
        data (dict): A dictionary containing the historical quotes data for the specified symbols, timeframe, and time range.
    """
    data=await get_historic_data_base(symbols, DataType.Quotes, start, end)
    return data



def get_data(symbols,start,end,timeframe,type="bins"):
    """
    Retrieves historical data for a given symbol, timeframe, and time range.

    Args:
        symbols (list): A list of symbols to retrieve historical data for.
        start (str): The start date of the historical data range in the format YYYY-MM-DD.
        end (str): The end date of the historical data range in the format YYYY-MM-DD.
        timeframe (TimeFrame): The timeframe of the historical data.
        type (str): The type of data to retrieve. Can be "bins", "trades", or "quotes". Defaults to "bins".

    Returns:
        data (dict): A dictionary containing the historical data for the specified symbols, timeframe, and time range.
    """
    start = pd.Timestamp(start, tz=NY).date().isoformat()
    end = pd.Timestamp(end,tz=NY).date().isoformat()
    timeframe: TimeFrame = timeframe

    if type == "bins":
        data=asyncio.run(get_historic_bars(symbols, start, end, timeframe))
    elif type == "trades":
        data=asyncio.run(get_historic_trades(symbols, start, end, timeframe))
    elif type ==  "quotes":
        data=asyncio.run(get_historic_quotes(symbols, start, end, timeframe))
    else:
        raise ValueError("Enter a valid input for type parameters valid inputs are [bins,trades,quotes]")

    return data


def get_assets(status="active"):
    """
    Retrieves assets with the given status.

    Args:
        status (str): The status of the assets to retrieve. Defaults to "active".

    Returns:
        assets (list): A list of assets with the given status.
    """
    return api.list_assets(status=status)



