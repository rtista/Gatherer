# Third-party Imports
from psycopg2 import OperationalError
from psycopg2.errors import SyntaxError, InvalidTextRepresentation, DuplicateSchema

# Batteries
from unittest import TestCase
from datetime import datetime

# Local imports
from adapters import PostgresAdapter


class TestPostgresAdapter(TestCase):
    """
    Testcase for the PostgresAdapter class.

    Args:
        TestCase (class): Testcase class.
    """

    # PostgresAdapter instance
    adapter = None

    def setUpClass():
        """
        Creates 'test' schema required for the tests.
        """
        adapter = PostgresAdapter('127.0.0.1', 'postgres')
        adapter.connect('postgres')
        try:
            adapter.execute('CREATE SCHEMA test;')
            adapter.execute('CREATE TABLE test.account( '
                                    'user_id serial PRIMARY KEY, '
                                    'username VARCHAR (50) NOT NULL, '
                                    'password VARCHAR (50) NOT NULL, '
                                    'email VARCHAR (355) NOT NULL, '
                                    'created_on TIMESTAMP NOT NULL, '
                                    'last_login TIMESTAMP);')
            adapter.commit()

        except DuplicateSchema:
                print('Test schema already created.')

        adapter.disconnect()

    def tearDownClass():
        """
        Drops 'test' schema required for the tests.
        """
        adapter = PostgresAdapter('127.0.0.1', 'postgres')
        adapter.connect('postgres')

        adapter.execute('DROP TABLE test.account')
        adapter.execute('DROP SCHEMA test')
        adapter.commit()
        adapter.disconnect()

    def setUp(self):
        """
        This will be executed before each test run.

        Instantiates an adapter for a localhost instance with the 'postgres' user.
        """
        self.adapter = PostgresAdapter('127.0.0.1', 'postgres')

    def tearDown(self):
        """
        This will be executed after each test run.
        """
        if self.adapter.isconnected():
            self.adapter.disconnect()

    def test_isconnected_success(self):
        """
        Tests the is connected method for a success scenario.
        """
        self.adapter.connect('postgres')
        self.assertTrue(self.adapter.isconnected(), 'Failed isconnected_success')

    def test_isconnected_failure(self):
        """
        Tests the is connected method for a failure scenario.
        """
        self.assertFalse(self.adapter.isconnected(), 'Failed isconnected_failure')

    def test_connect_success(self):
        """
        Tests the connection to the database.
        """
        self.adapter.connect('postgres')
        self.adapter.execute('SELECT 1;')

        # Check query execution result
        self.assertEqual(self.adapter.fetchone()[0], 1)

    def test_connect_failure(self):
        """
        Tests the connection to an unexistent database.
        """
        with self.assertRaises(OperationalError):
            self.adapter.connect('unexistent_database')

    def test_execute_success(self):
        """
        Test query execution success scenario.
        """
        self.adapter.connect('postgres')
        self.adapter.execute('SELECT 1;')

        # Check valid query result
        self.assertEqual(self.adapter.fetchone()[0], 1)

    def test_execute_failure_syntax(self):
        """
        Test query execution failure due to syntax error.
        """
        self.adapter.connect('postgres')

        # Check SyntaxError exception is raised
        with self.assertRaises(SyntaxError):
            self.adapter.execute('SELCT 1;')

    def test_executemany_success(self):
        """
        Tests bulk query execution success scenario.
        """
        self.adapter.connect('postgres')

        # Create three new entries
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = (
            ('john', 'johnpassword', 'john@domain.com', now),
            ('doe', 'doepassword', 'doe@domain.com', now),
            ('jane', 'janepassword', 'janedoe@domain.com', now)
        )

        self.adapter.executemany('INSERT INTO test.account(username, password, email, created_on, last_login) VALUES (%s, %s, %s, %s, NULL)', values)
        self.adapter.commit()

        # Check new entry count
        self.adapter.execute("""SELECT count(1) FROM test.account WHERE created_on = timestamp '{}'""".format(now))
        self.assertTrue(int(self.adapter.fetchone()[0]) == len(values))

    def test_executemany_syntax_failure(self):
        """
        Tests bulk query execution failure scenario due to wrong syntax.
        """
        self.adapter.connect('postgres')

        # Create three new entries
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = (
            ('john', 'johnpassword', 'john@domain.com', now),
            ('doe', 'doepassword', 'doe@domain.com', now),
            ('jane', 'janepassword', 'janedoe@domain.com', now)
        )

        with self.assertRaises(InvalidTextRepresentation):
            self.adapter.executemany('INSERT INTO test.account VALUES (%s, %s, %s, %s, NULL)', values)

    def test_fetchone_success(self):
        """
        Tests successful retrieval of one result from the query results.
        """
        self.adapter.connect('postgres')

        # Select one entry from the table
        self.adapter.execute('SELECT * FROM test.account LIMIT 1')
        entry = self.adapter.fetchone()

        # Check number of columns
        self.assertTrue(len(entry) == 6)

    def test_fetchone_empty_result(self):
        """
        Tests successful retrieval of an empty set from a query result.
        """
        self.adapter.connect('postgres')

        self.adapter.execute('SELECT * FROM test.account LIMIT 0')
        entry = self.adapter.fetchone()

        self.assertIsNone(entry)

    def test_fetchmany_success(self):
        """
        Tests retrieval of several results from a query.
        """
        self.adapter.connect('postgres')

        self.adapter.execute('SELECT * FROM test.account')

        entries = 0
        for _ in self.adapter.fetchmany(2):
            entries += 1

        self.assertTrue(entries == 2)

    def test_fetchall_success(self):
        """
        Tests retrieval of all results from a query.
        """
        self.adapter.connect('postgres')

        self.adapter.execute('SELECT * FROM test.account LIMIT 3')

        entries = 0
        for _ in self.adapter.fetchall():
            entries += 1

        self.assertTrue(entries == 3)

    def test_disconnect_success(self):
        """
        Tests disconnection from the database.
        """
        self.adapter.connect('postgres')
        self.adapter.disconnect()

        self.assertFalse(self.adapter.isconnected())
