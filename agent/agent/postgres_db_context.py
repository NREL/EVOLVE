"""" This module contains context class for interacting with PostGres DB."""

# Standard imports
import psycopg2

# third-party imports


# internal imports
class PostGresDB:
    """Class for managing interaction with PostGres DB."""

    def __init__(self, db_config: dict):
        """Constructor for DB.

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

    def __exit__(self, *args, **kwargs):
        self.connection.close()
