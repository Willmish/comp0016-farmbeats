from data_streamer.database_manager import DatabaseManager
import os
from dotenv import load_dotenv
import pyodbc


class GuiDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__("azure_db")
        load_dotenv()
        self._connection_string = os.getenv("DATABASE_CONNECTION_STRING")

    def __enter__(self):
        self._azure_conn = pyodbc.connect(self._connection_string)
        self._cursor = self._azure_conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self._azure_conn.close()

    def get_curr_val_single_subsys(self, subsys_name):
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
            return round(total / count, 2)
        else:
            return None

    def collect_curr_val(self):
        # [brightness, humidity, temperature, water]
        curr_vals = [
            self.get_curr_val_single_subsys("brightness"),
            self.get_curr_val_single_subsys("humidity"),
            self.get_curr_val_single_subsys("temperature"),
            self.get_curr_val_single_subsys("water_level"),
        ]
        return curr_vals

    def get_time_and_val_list(self, subsys_name):
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
        res = ""
        for row in self._cursor.execute("SELECT * FROM dbo.SensorData;"):
            res += str(row) + "\n"
        return res
