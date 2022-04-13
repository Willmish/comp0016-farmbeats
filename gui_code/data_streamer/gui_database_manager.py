import datetime
from typing import List, Tuple
from data_streamer.database_manager import DatabaseManager
import os
from dotenv import load_dotenv
import pyodbc


class GuiDatabaseManager(DatabaseManager):
    """
    GuiDatabaseManager directly communicates with the Azure Database to
    obtain specific data to be sent to the GUI system.

    :param DatabaseManager: Superclass of GuiDatabaseManager where
        all attributes are inherited from.
    :type DatabaseManager: DatabaseManager
    """

    def __init__(self):
        """
        __init__ creates an instance of GuiDatabaseManager.
        """
        super().__init__("azure_db")
        load_dotenv()
        self._connection_string = os.getenv("DATABASE_CONNECTION_STRING")

    def __enter__(self):
        """
        __enter__ connects with the Azure database and returns it.

        :return: Azure database being connected.
        :rtype: GuiDatabaseManager
        """
        self._azure_conn = pyodbc.connect(self._connection_string)
        self._cursor = self._azure_conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        """
        __exit__ closes the connection with Azure database.

        :param type: _description_
        :type type: _type_
        :param value: _description_
        :type value: _type_
        :param traceback: _description_
        :type traceback: _type_
        """
        self._azure_conn.close()

    def get_curr_val_single_subsys(self, subsys_name):
        """
        get_curr_val_single_subsys takes all sensor values from the
        same subsystem at the most recent timestamp and returns the
        average of these.

        :param subsys_name: Name of subsystem selected.
        :type subsys_name: str
        :return: Average most recent sensor value.
        :rtype: float
        """
        total = 0
        count = 0
        for row in self._cursor.execute(
            """
            SELECT  Value
            FROM dbo.SensorData a
            WHERE Timestamp = (SELECT MAX(Timestamp) """
            + "FROM dbo.SensorData b WHERE b.SensorType = '"
            + subsys_name
            + "') AND a.SensorType = '"
            + subsys_name
            + "';"
        ):
            total += row[0]
            count += 1
        if count > 0:
            return round(total / count, 2)
        else:
            return None

    def get_curr_actuation_val_single_subsys(self, subsys_name):
        """
        get_curr_actuation_val_single_subsys takes all actuator values from the
        same subsystem at the most recent timestamp and returns the
        average of these.

        :param subsys_name: Name of subsystem selected.
        :type subsys_name: str
        :return: Average most recent actuator value.
        :rtype: float
        """
        total = 0
        count = 0
        for row in self._cursor.execute(
            """
            SELECT ActuatorValue
            FROM dbo.SensorData a
            WHERE Timestamp = (SELECT MAX(Timestamp) """
            + "FROM dbo.SensorData b WHERE b.SensorType = '"
            + subsys_name
            + "'AND b.ActuatorValue IS NOT NULL) AND a.SensorType = '"
            + subsys_name
            + "';"
        ):
            total += row[0]
            count += 1
        if count > 0:
            val = round(total / count, 2)
            if val > 0:
                return val
            else:
                return 0
        else:
            return None

    def get_time_and_val_list(
        self, subsys_name
    ) -> Tuple[List[int], List[datetime.datetime]]:
        """
        get_time_and_val_list gets a list of times and sensor
        values based on the subsystem name.

        :param subsys_name: Name of subsystem selected.
        :type subsys_name: str
        :return: Tuple of list of values with list of timestamps.
        :rtype: tuple(list(int), list(DateTime))
        """
        vals = []
        times = []

        for row in self._cursor.execute(
            """
            SELECT  Value, Timestamp
            FROM dbo.SensorData """
            + "WHERE SensorType = '"
            + subsys_name
            + "';"
        ):
            vals.append(row[0])
            times.append(row[1])
        return (vals, times)

    def __repr__(self) -> str:
        """
        __repr__ represents this class object as a string.

        :return: String representation of GuiDatabaseManager.
        :rtype: str
        """
        res = ""
        for row in self._cursor.execute("SELECT * FROM dbo.SensorData;"):
            res += str(row) + "\n"
        return res
