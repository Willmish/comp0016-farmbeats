import sys
sys.path.insert(0, "..")
from data_streamer.gui_database_manager import GuiDatabaseManager
import unittest
from os.path import exists
import pyodbc
import os
from dotenv import load_dotenv
from tools.exceptions import EnvFileMissingException


class TestDatabaseResponse(unittest.TestCase):
    DEFAULT_TIMEOUT = 3

    def test_proper_connection(self):
        load_dotenv("../../.env")
        db = GuiDatabaseManager("../../.env", 5)
        self.assertIsNotNone(db.__enter__())
        if hasattr(db, "_azure_conn"):
            db._azure_conn.close()

    def test_wrong_server_name(self):
        f = open(".env", "w+")
        f.write(
            'DATABASE_CONNECTION_STRING="DRIVER={ODBC Driver 18 for ' +
            'SQL Server};' +
            'SERVER=wrong_name:wrong_name;PORT=1433;DATABASE=wrong_name;' +
            'UID=wrong_name;PWD={}"'
        )
        f.close()

        db = GuiDatabaseManager("./.env", self.DEFAULT_TIMEOUT)
        self.assertRaises(pyodbc.Error, db.__enter__)
        if hasattr(db, "_azure_conn"):
            db._azure_conn.close()

    def test_empty_file(self):
        f = open(".env", "w+")
        f.write("")
        f.close()
        self.assertRaises(
            EnvFileMissingException,
            GuiDatabaseManager,
            "./.env",
            self.DEFAULT_TIMEOUT,
        )

    def test_non_existing_file(self):
        self.assertRaises(
            EnvFileMissingException,
            GuiDatabaseManager,
            "./.env",
            self.DEFAULT_TIMEOUT,
        )

    def tearDown(self) -> None:
        if exists(".env"):
            os.remove(".env")
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
