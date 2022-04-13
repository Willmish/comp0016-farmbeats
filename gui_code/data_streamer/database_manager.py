import sqlite3
from pubsub import pub


class DatabaseManager:
    """_summary_"""

    sensor_data_topic = "sensor_data"

    def __init__(self, database_path: str = "test.db"):
        """
        __init__ creates an instance of DatabaseManager.

        :param database_path: _description_, defaults to "test.db"
        :type database_path: str, optional
        """
        self._database_path: str = database_path
        self._connection = None
        self._cursor = None
        pub.subscribe(
            self.sensor_data_listener, DatabaseManager.sensor_data_topic
        )

    def __enter__(self):
        """
        __enter__ connects with the sqlite database and returns it.

        :return: Sqlite database being connected.
        :rtype: DatabaseManager
        """
        self._connection = sqlite3.connect(self._database_path)
        self._cursor = self._connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
        """
        __exit__ closes the connection with sqlite database.

        :param type: _description_
        :type type: _type_
        :param value: _description_
        :type value: _type_
        :param traceback: _description_
        :type traceback: _type_
        """
        self._connection.close()

    def create_sensor_data_table(self):
        """
        create_sensor_data_table creates a table in sqlite database
        with the following structure.

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
        """
        add_sensor_data

        :param timestamp: Time at which sensor value is taken.
        :type timestamp: DateTime
        :param sensor_id: Unique sensor ID for current sensor.
        :type sensor_id: int
        :param sensor_type: Sensor type corresponding to
            specific subsystem.
        :type sensor_type: str
        :param sensor_value: Value collected from sensor
        :type sensor_value: float

        """
        self._cursor.execute(
            """
                INSERT INTO SensorData VALUES (?, ?, ?, ?)
                """,
            (timestamp, sensor_id, sensor_type, sensor_value),
        )
        self._connection.commit()

    def _remove_data_by_id_type(self, sensor_id, sensor_type):
        """
        _remove_data_by_id_type removes row from databased with
        corresponding sensor id and type.

        :param sensor_id: Sensor ID.
        :type sensor_id: int
        :param sensor_type: Type of sensor.
        :type sensor_type: str
        """
        self._cursor.execute(
            """
                DELETE FROM SensorData WHERE (SensorID = ?) AND SensorType = ?
                """,
            (sensor_id, sensor_type),
        )
        self._connection.commit()

    def sensor_data_listener(self, args):
        """
        sensor_data_listener receives data over pubsub.

        :param args: _description_
        :type args: _type_
        """
        print("Received data over pubsub: ", args)
        self.add_sensor_data(
            args.timestamp, args.sensor_id, args.sensor_type, args.sensor_value
        )

    def __repr__(self) -> str:
        """
        __repr__ represents this class object as a string.

        :return: String representation of DatabaseManager.
        :rtype: str
        """
        res = ""
        for row in self._cursor.execute("SELECT * FROM SensorData;"):
            res += str(row) + "\n"
        return res
