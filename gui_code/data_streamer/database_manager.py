import sqlite3
from pubsub import pub


# Copied from src folder for now


class DatabaseManager:
    sensor_data_topic = "sensor_data"

    def __init__(self, database_path: str = "test.db"):
        self._database_path: str = database_path
        self._connection = None
        self._cursor = None
        pub.subscribe(
            self.sensor_data_listener, DatabaseManager.sensor_data_topic
        )

    def __enter__(self):
        self._connection = sqlite3.connect(self._database_path)
        self._cursor = self._connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self._connection.close()

    def create_sensor_data_table(self):
        """
        Table structure:
        +-----------+----------+------------+-------+
        | Timestamp | SensorID | SensorType | Value |
        +-----------+----------+------------+-------+
        |  INTEGER  | INTEGER  |    TEXT    |  REAL |
        +-----------+----------+------------+-------+
        """
        self._cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS SensorData(
                Timestamp INTEGER,
                SensorID INTEGER,
                SensorType TEXT,
                Value REAL,
                PRIMARY KEY(Timestamp, SensorID)
                );
                """
        )
        self._connection.commit()

    def add_sensor_data(
        self, timestamp, sensor_id: int, sensor_type: str, sensor_value: float
    ):
        self._cursor.execute(
            """
                INSERT INTO SensorData VALUES (?, ?, ?, ?)
                """,
            (timestamp, sensor_id, sensor_type, sensor_value),
        )
        self._connection.commit()

    def _remove_data_by_id_type(self, sensor_id, sensor_type):
        self._cursor.execute(
            """
                DELETE FROM SensorData WHERE (SensorID = ?) AND SensorType = ?
                """,
            (sensor_id, sensor_type),
        )
        self._connection.commit()

    def sensor_data_listener(self, args):
        print("Received data over pubsub: ", args)
        self.add_sensor_data(
            args.timestamp, args.sensor_id, args.sensor_type, args.sensor_value
        )

    def __repr__(self) -> str:
        res = ""
        for row in self._cursor.execute("SELECT * FROM SensorData;"):
            res += str(row) + "\n"
        return res

