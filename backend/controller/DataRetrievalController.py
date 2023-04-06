import sys
import pathlib
import json
from typing import List
from sqlalchemy.orm import Session
from db.dbconnect import connect_to_database


class DataRetrievalController:
    """
    Class for managing the retrieval of data from the database.
    """

    def __init__(self):
        """
        Constructor for the DataRetrievalController class. Initializes a session to connect to the database.
        """
        self.session = connect_to_database()

    def query_data(self, mapper, parameter_val=None, parameter="id"):
        """
        Queries data from the database using the given mapper, parameter value, and parameter name.

        Args:
            mapper: The mapper object for the type of data to retrieve.
            parameter_val: The value of the parameter to filter on.
            parameter: The name of the parameter to filter on.

        Returns:
            res (list): A list of dictionary representations of the retrieved data.
        """
        session = self.session()
        if type(parameter_val) == str:
            q_res = session.query(mapper).filter(getattr(mapper, parameter) == parameter_val).all()
            res = [q.toDict() for q in q_res]
            return res
        elif type(parameter_val) == list:
            prm = getattr(mapper, parameter)
            q_res = session.query(mapper).filter(prm.in_(parameter_val)).all()
            res = [q.toDict() for q in q_res]
            return res
        elif parameter_val == None:
            q_res = session.query(mapper).all()
            res = [q.toDict() for q in q_res]
            return res
        else:
            print("Enter valid parameter value. List is valid type.")

    def get_latest_series(self, mapper, parameter_val=None, parameter="id"):
        """
        Gets the latest series data from the database using the given mapper, parameter value, and parameter name.

        Args:
            mapper: The mapper object for the type of data to retrieve.
            parameter_val: The value of the parameter to filter on.
            parameter: The name of the parameter to filter on.

        Returns:
            res (dict): A dictionary representation of the latest series data for the given parameters.
        """
        session = self.session()
        if type(parameter_val) == str:
            q_res = session.query(mapper).filter(getattr(mapper, parameter) == parameter_val).order_by(mapper.date.desc()).first()
            res = q_res.toDict()
            return res
        elif type(parameter_val) == list:
            prm = getattr(mapper, parameter)
            q_res = session.query(mapper).filter(prm.in_(parameter_val)).order_by(mapper.date.desc()).first()
            res = q_res.toDict()
            return res
        elif parameter_val == None:
            q_res = session.query(mapper).order_by(mapper.date.desc()).first()
            res = q_res.toDict()
            return res
        else:
            print("Enter valid parameter value. List is valid type.")
