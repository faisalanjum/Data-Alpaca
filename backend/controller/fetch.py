import sys
import pathlib

# Add parent directory to sys.path to access DataRetrievalController
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2])) 

from DataRetrievalController import DataRetrievalController 
from db.models import BarDaily, BarMinute, BarHour, Trades, Quotes, Stocks


def get_stock_by_symbol(symbol: str):
    """
    Retrieves the stock data for a given symbol.

    Args:
        symbol (str): The symbol of the stock to retrieve.

    Returns:
        data (list): A list of Stocks objects representing the stock data for the given symbol.
    """
    try:
        data_ret_obj = DataRetrievalController()
        data = data_ret_obj.query_data(Stocks, symbol, "symbol")
        return data
    except Exception as e:
        raise e


def get_bars_hour_by_symbol(symbol: str):
    """
    Retrieves the hourly bar data for a given symbol.

    Args:
        symbol (str): The symbol of the stock to retrieve bar data for.

    Returns:
        data (list): A list of BarHour objects representing the hourly bar data for the given symbol.
    """
    try:
        data_ret_obj = DataRetrievalController()
        data = data_ret_obj.query_data(BarHour, symbol, "ticker")
        return data
    except Exception as e:
        raise e


def get_bars_min_by_symbol(symbol: str):
    """
    Retrieves the minute bar data for a given symbol.

    Args:
        symbol (str): The symbol of the stock to retrieve bar data for.

    Returns:
        data (list): A list of BarMinute objects representing the minute bar data for the given symbol.
    """
    try:
        data_ret_obj = DataRetrievalController()
        data = data_ret_obj.query_data(BarMinute, symbol, "ticker")
        return data
    except Exception as e:
        raise e


def get_bars_day_by_symbol(symbol: str):
    """
    Retrieves the daily bar data for a given symbol.

    Args:
        symbol (str): The symbol of the stock to retrieve bar data for.

    Returns:
        data (list): A list of BarDaily objects representing the daily bar data for the given symbol.
    """
    try:
        data_ret_obj = DataRetrievalController()
        data = data_ret_obj.query_data(BarDaily, symbol, "ticker")
        return data
    except Exception as e:
        raise e


def get_trades_by_symbol(symbol: str):
    """
    Retrieves the trade data for a given symbol.

    Args:
        symbol (str): The symbol of the stock to retrieve trade data for.

    Returns:
        data (list): A list of Trades objects representing the trade data for the given symbol.
    """
    try:
        data_ret_obj = DataRetrievalController()
        data = data_ret_obj.query_data(Trades, symbol, "ticker")
        return data
    except Exception as e:
        raise e


def get_quotes_by_symbol(symbol: str):
    """
    Retrieves the quote data for a given symbol.

    Args:
        symbol (str): The symbol of the stock to retrieve quote data for.

    Returns:
        data (list): A list of Quotes objects representing the quote data for the given symbol.
    """
    try:
        data_ret_obj = DataRetrievalController()
        data = data_ret_obj.query_data(Quotes, symbol, "ticker")
        return data
    except Exception as e:
        raise e

# Example usage:
# data = get_bars_min_by_symbol("
