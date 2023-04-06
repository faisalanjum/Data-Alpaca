from models import Quotes, Stocks, BarHour, BarMinute, BarDaily, Trades
from api import get_assets, get_data
from alpaca_trade_api.rest import TimeFrame
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import requests
import pandas as pd
import sys
import pathlib
import os
import models
import time
import json
from helpers import insert_into_database
from dbconnect import connect_to_database
from dotenv import load_dotenv

# Load the environment variables from a .env file
load_dotenv()

# Set the timezone for New York
NY = 'America/New_York'

def populate_assets(status="active"):
    """
    Populates the database with stock assets.

    Args:
        status (str): Filter for the asset status. Can be "active", "inactive", or "delisted".
                      Defaults to "active".
    """
    assets = get_assets(status=status)
    assets = [a.__dict__ for a in assets]
    asset_df = pd.DataFrame.from_dict(assets)
    asset_df = pd.DataFrame(asset_df.pop('_raw').values.tolist())
    asset_df = asset_df.loc[:, ['id', 'class', 'exchange', 'symbol', 'name', 'status', 'tradable',
                                'marginable', 'shortable', 'easy_to_borrow']]
    asset_df.rename(columns={"class": "type"}, inplace=True)
    insert_into_database(Stocks, asset_df.to_dict(orient="records"))


def populate_asset_data(symbols, start, end, timeframe=TimeFrame.Minute, typ="bins"):
    """
    Populates the database with data for a list of stock symbols.

    Args:
        symbols (list): A list of stock symbols to retrieve data for.
        start (str): The start date in the format YYYY-MM-DD.
        end (str): The end date in the format YYYY-MM-DD.
        timeframe (alpaca_trade_api.rest.TimeFrame): The timeframe of the data. Defaults to TimeFrame.Minute.
        typ (str): The type of data to retrieve. Can be "bins", "trades", or "quotes". Defaults to "bins".
    """
    data = get_data(symbols, start, end, timeframe, typ)
    db_engine = connect_to_database()
    ssn = db_engine()
    dfs=[]
    for d in data:

        data_df = pd.DataFrame.from_dict(d[1])

        if data_df.empty == False:
            # Add the ticker to the dataframe
            data_df["ticker"] = d[0]
            data_df.reset_index(inplace=True)
            dfs.append(data_df)

            if typ == "bins":
                # Set the model based on the timeframe
                if timeframe == TimeFrame.Minute:
                    model=BarMinute
                elif timeframe == TimeFrame.Day:
                    model=BarDaily
                elif timeframe == TimeFrame.Hour:
                    model=BarHour

            elif typ == "trades":
                # Rename the "id" column to "trade_id"
                data_df.rename(columns={"id": "trade_id"}, inplace=True)
                model=Trades
                
                # Remove duplicates based on trade_id, ticker, timestamp, exchange, price, size, and tape
                data_df=data_df.drop_duplicates(subset=["trade_id",'ticker', "timestamp","exchange","price","size","tape"])
                dfs.append(data_df ) 
                
                # Convert the timestamp to New York time zone
                # data_df['timestamp'] = pd.to_datetime(data_df['timestamp'],unit='ns')
                # data_df.timestamp = data_df.timestamp.dt.tz_localize('UTC').dt.tz
