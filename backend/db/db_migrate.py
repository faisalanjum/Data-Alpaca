from dbconnect import connect_to_database
from models import Base


def migrate_models():
    """
    Function to migrate database models

    Returns:
    None
    """
    engine = connect_to_database(get_engine_only=True)
    try:
        Base.metadata.create_all(engine)
        print("migrations completed")
    except Exception as e:
        raise e


def clean_db():
    """
    Function to clean the database

    Returns:
    None
    """
    engine = connect_to_database(get_engine_only=True)
    try:
        Base.metadata.drop_all(engine)
        print("database cleaned completed")
    except Exception as e:
        raise e


clean_db()
migrate_models()
