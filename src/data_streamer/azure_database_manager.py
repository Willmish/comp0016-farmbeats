from pubsub import pub
from database_manager import DatabaseManager
from dotenv import load_dotenv
from tools.logging import logInfo
import os
import pyodbc


class AzureDatabaseManager(DatabaseManager):
    sensor_data_topic = "database_update.actuator"

    def __init__(self, database_path: str = "test.db"):
        super().__init__("azure_db")
        load_dotenv()
        self._connection_string = os.getenv("DATABASE_CONNECTION_STRING")

    def __enter__(self):
        self._azure_conn = pyodbc.connect(self._connection_string)
        self._cursor = self._azure_conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self._azure_conn.close()

    def create_sensor_data_table(self):
        """
        Table structure:
        +-----------+----------+------------+-------+---------------+
        | Timestamp | SensorID | SensorType | Value | ActuatorValue |
        +-----------+----------+------------+-------+---------------+
        |  INTEGER  | INTEGER  |    TEXT    |  REAL |      REAL     |
        +-----------+----------+------------+-------+---------------+
        |  VALUE    | VALUE    |    VALUE   | VALUE |     [NULL]    |
        +-----------+----------+------------+-------+---------------+
        """
        self._cursor.execute(
            """
                IF OBJECT_ID('dbo.SensorData', 'U') IS  NULL
                CREATE TABLE dbo.SensorData
                (
                    [Timestamp] DATETIME NOT NULL,
                    [SensorID] INT NOT NULL,
                    [SensorType] VARCHAR(256) NOT NULL,
                    [Value] REAL NOT NULL,
                    [ActuatorValue] REAL,
                    CONSTRAINT SensorData_pk PRIMARY KEY (Timestamp, SensorID,
                    SensorType)

                );
                """
        )
        self._azure_conn.commit()

    def add_sensor_data(
        self,
        timestamp,
        sensor_id: int,
        sensor_type: str,
        sensor_value: float,
        actuator_value: float,
    ):
        self._cursor.execute(
            """
                INSERT INTO dbo.SensorData VALUES (?, ?, ?, ?, ?)
                """,
            (timestamp, sensor_id, sensor_type, sensor_value, actuator_value),
        )
        self._azure_conn.commit()

    def _remove_data_by_id_type(self, sensor_id, sensor_type):
        self._cursor.execute(
            """
                DELETE FROM dbo.SensorData
                WHERE SensorID = ? AND SensorType = ?
                """,
            (sensor_id, sensor_type),
        )
        self._azure_conn.commit()

    def sensor_data_listener(self, args):
        logInfo("Received data over pubsub: ", args)
        self.add_sensor_data(
            args.timestamp,
            args.sensor_id,
            args.sensor_type,
            args.sensor_value,
            args.actuator_value,
        )

    def __repr__(self) -> str:
        res = ""
        for row in self._cursor.execute("SELECT * FROM dbo.SensorData;"):
            res += str(row) + "\n"
        return res


if __name__ == "__main__":
    # Test the DB, and clean up afterwards.
    # Should print the whole db with new test entry added
    import sys
    from time import sleep
    from datetime import datetime

    sys.path.insert(0, "..")
    from tools.sensor_data import SensorData

    def get_current_time_iso_cut():
        # Get current time in ISO format,
        # ODBC acceptable (without fractional seconds)
        date = datetime.now().isoformat()
        return date[: date.find(".")]

    with AzureDatabaseManager() as db:
        db.create_sensor_data_table()
        print(get_current_time_iso_cut())
        pub.sendMessage(
            "actuator",
            args=SensorData(
                get_current_time_iso_cut(), -1, "test_sensor_type", -999, 50
            ),
        )

        val = 0
        for x in range(3):
            pub.sendMessage(
                "actuator",
                args=SensorData(
                    get_current_time_iso_cut(), 1, "brightness", 900 + val, 50
                ),
            )
            pub.sendMessage(
                "actuator",
                args=SensorData(
                    get_current_time_iso_cut(), 2, "humidity", 55 + val, 50
                ),
            )
            pub.sendMessage(
                "actuator",
                args=SensorData(
                    get_current_time_iso_cut(), 3, "temperature", 20 + val, 50
                ),
            )
            pub.sendMessage(
                "actuator",
                args=SensorData(
                    get_current_time_iso_cut(), 4, "water level", 15 + val, 50
                ),
            )
            val += 1

            sleep(1)

        print(db)
        db._remove_data_by_id_type(-1, "test_sensor_type")
        print(db)
