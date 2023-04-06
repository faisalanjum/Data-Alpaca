import sys,os,pathlib
# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  BigInteger, inspect,MetaData
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint, ForeignKey, Boolean, Float, Enum,TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.event import listens_for
import enum
from dotenv import load_dotenv
load_dotenv()
meta_obj=MetaData(schema=os.getenv("POSTGRES_SCHEMA"))

Base = declarative_base(metadata=meta_obj)


class Stocks(Base):

    #table_name
    __tablename__="stocks"

    #primary
    id=Column("id",String,)
    #columns
    type=Column("type",String)
    exchange=Column("exchange",String)
    symbol=Column("symbol",String,primary_key=True)
    name=Column("name",String)
    status=Column("status", String)
    tradable=Column("tradable",String)
    marginable=Column("marginable",String)
    shortable=Column("shortable",String)
    easy_to_borrow=Column("easy_to_borrow'",String)
    
    # relationships
    prices_min=relationship("BarMinute",backref="stocks",order_by="desc(BarMinute.timestamp)",lazy="dynamic")
    prices_hour=relationship("BarHour",backref="stocks",order_by="desc(BarHour.timestamp)",lazy="dynamic")
    prices_daily=relationship("BarDaily",backref="stocks",order_by="desc(BarDaily.timestamp)",lazy="dynamic")
    trades=relationship("Trades",backref="stocks",order_by="desc(Trades.timestamp)",lazy="dynamic")
    quotes=relationship("Quotes",backref="stocks",order_by="desc(Quotes.timestamp)",lazy="dynamic")
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class BarMinute(Base):
    #table_name
    __tablename__="bars_minute"
    
    #foreign_key
    ticker=Column("ticker",ForeignKey('stocks.symbol',onupdate='CASCADE'),primary_key=True)
    
    #primary
    timestamp=Column("timestamp",TIMESTAMP,primary_key=True)
    open=Column("open",Float)
    high=Column("high",Float)
    low=Column("low",Float)
    close=Column("close",Float)
    volume=Column("volume",Float)
    trade_count=Column("trade_count",Integer)
    vwap=Column("vwap",Float)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

  

class BarHour(Base):

    #table_name
    __tablename__="bars_hour"
    
    #constraint
    __table_args__ = tuple([UniqueConstraint('ticker', "timestamp")])
    
    #foreign_key
    ticker=Column("ticker",ForeignKey('stocks.symbol',onupdate='CASCADE'),primary_key=True)
    
    #primary
    timestamp=Column("timestamp",TIMESTAMP,primary_key=True)
    open=Column("open",Float)
    high=Column("high",Float)
    low=Column("low",Float)
    close=Column("close",Float)
    volume=Column("volume",Float)
    trade_count=Column("trade_count",Integer)
    vwap=Column("vwap",Float)
    


    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }



class BarDaily(Base):

    #table_name
    __tablename__="bars_daily"
   
    #foreign_key
    
    ticker=Column("ticker",ForeignKey('stocks.symbol',onupdate='CASCADE'),primary_key=True)


    #primary
    timestamp=Column("timestamp",TIMESTAMP,primary_key=True)
    open=Column("open",Float)
    high=Column("high",Float)
    low=Column("low",Float)
    close=Column("close",Float)
    volume=Column("volume",Float)
    trade_count=Column("trade_count",Integer)
    vwap=Column("vwap",Float)
    


    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

  



class Exch(enum.Enum):
    A = "NYSE American (AMEX)"
    B = "NASDAQ OMX BX"
    C = "NAtional Stock Exchange"
    D = "FINRA ADF"
    E = "Market Independent"
    H = "MIAX"
    I = "International Securities Exchange"
    J = "Cboe EDGA"
    K = "Cboe EDGX"
    L = "Long Term Stock Exchange"
    M = "Chicago Stock Exchange"
    N = "New York Stock Exchange"
    P = "NYSE Arca"
    Q = "NASDAQ OMX"
    S = "NASDAQ Small Cap"
    T = "NASDAQ Int"
    U = "Members Exchange"
    V = "IEX"
    W = "CBOE"
    X = "NASDAQ OMX PSX"
    Y = "CboeBYX"
    Z = "CboeBZX"
    NA = "NotKnown"




class Trades(Base):
    #table_name
    __tablename__="trades"
    #foreign_key 
    ticker=Column(ForeignKey('stocks.symbol',onupdate='CASCADE'))
    __table_args__ = tuple([UniqueConstraint("trade_id",'ticker', "timestamp","exchange","price","size","tape")])

    #primary_key



    #columns
    timestamp=Column("timestamp",TIMESTAMP,primary_key=True)
    exchange=Column("exchange",Enum(Exch),primary_key=True)
    price=Column("price",Float)
    size=Column("size",Float)
    conditions=Column("conditions",postgresql.ARRAY(String))
    tape=Column("tape",String)
    trade_id=Column("trade_id",BigInteger,primary_key=True)
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }



class Quotes(Base):
    #table_names
    __tablename__="quotes"

   
    #foreign_key 
    ticker=Column(ForeignKey('stocks.symbol',onupdate='CASCADE'),primary_key=True)
    timestamp=Column("timestamp",TIMESTAMP,primary_key=True)
    ask_exchange=Column("ask_exchange",String,primary_key=True,default="NOTKNOWN")
    ask_price=Column("ask_price",Float,primary_key=True)
    ask_size=Column("ask_size",BigInteger,primary_key=True)
    bid_exchange=Column("bid_exchange",String,primary_key=True ,default="NOTKNOWN")
    bid_price=Column("bid_price",Float,primary_key=True)
    bid_size=Column("bid_size",BigInteger,primary_key=True)
    conditions=Column("conditions",postgresql.ARRAY(String),)
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }



class Crons(Base):
    #table_names
    __tablename__="crons"

    #constraint
    __table_args__ = tuple([UniqueConstraint('cron_id')])
 
    #primary_key
    id=Column(Integer,index=True,primary_key=True,autoincrement=True)

    #foreign_key 
    cron_id=Column("cron_id",String)
    cron_type=Column("cron_type",String)
    cron_on=Column("cron_on",String)
    started_at=Column("created_at",DateTime(timezone=True),server_default=func.now())
    completed_at=Column("updated_at",DateTime(timezone=True),server_default=func.now())
    cron_status=Column("cron_status",String)
   
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
