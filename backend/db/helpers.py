from sqlite3 import IntegrityError
from dbconnect import connect_to_database

def insert_into_database(mapper, data, ssn=None):
    """
    Inserts or updates records into a database using the provided mapper and data.

    Parameters:
    mapper (class): The SQLAlchemy mapper for the table to insert data into.
    data (list): A list of dictionaries representing the data to insert.
    ssn (Session): Optional SQLAlchemy Session object to use for the transaction.

    Returns:
    None

    """
    # If a Session object is not provided, connect to the database and create one
    if ssn is None:
        db_engine = connect_to_database()
        ssn = db_engine()

    try:
        # Attempt to insert the data into the database
        ssn.bulk_insert_mappings(mapper, data)
        ssn.commit()
        print("Records added")

    except:
        # If inserting fails, roll back the transaction and try updating instead
        ssn.rollback()
        try:
            print("Updating records")
            ssn.bulk_update_mappings(mapper, data)
            ssn.commit()
            print("Records updated")
        except IntegrityError as e:
            # If updating fails due to an integrity error, print an error message
            print("There was an error adding data to the database:\n{}".format(e))
