"""" This module contains context class for interacting with PostGres DB."""

# Standard imports
import psycopg2
from typing import Dict

# third-party imports

# internal imports
class PostGresDB:
    """ Class for managing interaction with PostGres DB. """
    
    def __init__(self,
        db_config: Dict
    ):
        """ Constructor for DB.

        e.g. db_config = {
            user: str, 
            password: str, 
            host: str, 
            port: str, 
            database: str
        }
        
        """
        self.connection = psycopg2.connect(**db_config)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.connection.close()
    