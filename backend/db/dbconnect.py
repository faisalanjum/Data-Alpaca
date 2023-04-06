import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#load the env variables
load_dotenv()

def connect_to_database(get_engine_only=False):
    """
    Connect to a database using the DB_URL environment variable.

    Args:
        get_engine_only (bool, optional): If True, return only the SQLAlchemy engine object. If False (default), 
            return a SQLAlchemy session object.

    Returns:
        session or engine: A SQLAlchemy session object or engine object, depending on the value of get_engine_only.

    Raises:
        ConnectionError: If there is an error connecting to the database.
    """

    try:
        # Get the DB_URL from the environment variables
        db_url = os.environ["DB_URL"]
        # Create a SQLAlchemy engine object with the DB_URL
        engine = create_engine(str(db_url), echo=False)

        if get_engine_only:
            # If get_engine_only is True, return only the engine object
            return engine
        
        # Otherwise, create a session factory object that uses the engine object
        session = sessionmaker(engine, expire_on_commit=False)
        print("Connection Established!")
        # Return the session factory object
        return session

    except Exception as e:
        # If there is an error connecting to the database, raise a ConnectionError
        raise ConnectionError("There is some error connecting to data base")
