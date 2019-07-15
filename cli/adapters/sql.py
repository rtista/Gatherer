# Third-party imports
import psycopg2
import MySQLdb

# Local imports
from .abstract import SQLDBAdapter


class PostgresAdapter(SQLDBAdapter):
    """
    Provides a simple API for a PostgreSQL database.
    
    Args:
        SQLDBAdapter (class): An adapter for SQL based databases.
    """
    def __init__(self, host, username, port=5432, password=None):
        """
        Creates a PostgresAdapter instance.
        
        Args:
            host (str): The hostname or IP address for the DB instance.
            port (int, optional): The port to which to connect. Defaults to 5432.
            username (str): The username to be used in authentication.
            password (str, optional): The password to be used in authentication. Defaults to None.
        """
        super().__init__(host, port, username, password)

    def isconnected(self):
        """
        Returns whether the connection to the database is alive.

        Raises:
            NotImplementedError: When the method is not implemented.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            return False

        return True

    def connect(self):
        """
        Connects to the database instance.

        Raises:
            NotImplementedError: When the method is not implemented.
        """
        self._connection = psycopg2.connect(host=self._host, port=self._port, 
                                            user=self._username, password=self._password)

        # Create cursor upon connecting
        self._cursor = self._connection.cursor()

    def execute(self, query):
        """
        Executes an SQL query against the database.

        Args:
            query (str): The query to be executed.

        Raises:
            Exception: When the adapter is not connected to the database.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            raise Exception('Not connected to the database.')

        # Execute query
        self._cursor.execute(query)

    def executemany(self, query, values, page_size=100):
        """
        Executes a Batch SQL query against the database.

        Args:
            query (str): The query to be executed.
            values (tuple): Tuple of tuples of values to be replaced in the query.
            page_size (int, optional): The page_size for the PostgreSQL instance batch queries. Defaults to 100.

        Raises:
            Exception: When the adapter is not connected to the database.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            raise Exception('Not connected to the database.')

        # Execute batch query
        psycopg2.extras.execute_batch(self._cursor, query, values, page_size)

    def commit(self):
        """
        Commits changes to the database, making them persistent.

        Raises:
            Exception: When the adapter is not connected to the database.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            raise Exception('Not connected to the database.')

        self._connection.commit()

    def fecthone(self):
        """
        Retrieves one row for the results of the most recently
        executed query.

        Raises:
            Exception: When the adapter is not connected to the database.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            raise Exception('Not connected to the database.')

        return self._cursor.fecthone()

    def fecthall(self):
        """
        Retrieves an iterator for the results of the most recently
        executed query.

        Raises:
            Exception: When the adapter is not connected to the database.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            raise Exception('Not connected to the database.')

        return self._cursor.fecthall()

    def disconnect(self):
        """
        Disconnects from the database instance.

        Raises:
            Exception: When the adapter is not connected to the database.
        """
        # Check if cursor is instantiated
        if not self._cursor:
            raise Exception('Not connected to the database.')

        self._cursor.close()
        self._connection.close()