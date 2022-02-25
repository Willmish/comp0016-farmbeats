from pubsub import pub
from database_manager import DatabaseManager
import pyodbc


server = 'iot-farmbeats.database.windows.net'
database = 'iot-farmbeats'
username = 'iotFarmBeats2022'
password = '{plantGrowth22}'
driver = '{ODBC Driver 18 for SQL Server}'

class AzureDatabaseManager(DatabaseManager):
    sensor_data_topic = "sensor_data"

    def __init__(self, database_path: str = "test.db"):
        super().__init__('azure_db')

    def __enter__(self):
        self._azure_conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
        self._cursor =  self._azure_conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self._azure_conn.close()

    def create_sensor_data_table(self):
        '''
        Table structure:
        +-----------+----------+------------+-------+
        | Timestamp | SensorID | SensorType | Value |
        +-----------+----------+------------+-------+
        |  INTEGER  | INTEGER  |    TEXT    |  REAL |
        +-----------+----------+------------+-------+
        '''
        self._cursor.execute(
                '''
                IF OBJECT_ID('dbo.SensorData', 'U') IS  NULL
                CREATE TABLE dbo.SensorData
                (
                    [Timestamp] INT NOT NULL,
                    [SensorID] INT NOT NULL,
                    [SensorType] TEXT NOT NULL,
                    [Value] REAL NOT NULL,
                    CONSTRAINT SensorData_pk PRIMARY KEY (Timestamp, SensorID)
                );
                ''')
        self._azure_conn.commit()

    def add_sensor_data(self, timestamp, sensor_id: int, sensor_type: str,
                        sensor_value: float):
        self._cursor.execute(
                '''
                INSERT INTO SensorData VALUES (?, ?, ?, ?)
                ''', (timestamp, sensor_id, sensor_type, sensor_value)
                )
        self._azure_conn.commit()

    def _remove_data_by_id_type(self, sensor_id, sensor_type):
        print ("sensor id type: " + str(type(sensor_id)))
        print ("sensor type type: " + str(type(sensor_type)))
        self._cursor.execute(
                '''
                DELETE FROM SensorData WHERE SensorID = ? AND SensorType = ?
                ''', (sensor_id, sensor_type)
                )
        self._azure_conn.commit()

    def sensor_data_listener(self, args):
        print("Received data over pubsub: ", args)
        self.add_sensor_data(args.timestamp, args.sensor_id,
                             args.sensor_type, args.sensor_value)

    def __repr__(self) -> str:
        res = ''
        for row in self._cursor.execute("SELECT * FROM SensorData;"):
            res += str(row) + '\n'
        return res


if __name__ == "__main__":
    # Test the DB, and clean up afterwards.
    # Should print the whole db with new test entry added
    import sys
    from time import time
    sys.path.insert(0, '..')
    from tools.sensor_data import SensorData
    with AzureDatabaseManager() as db:
        db.create_sensor_data_table()
        pub.sendMessage("sensor_data", args=SensorData(time(),
                        -1, "test_sensor_type", -999))
        print(db)
        db._remove_data_by_id_type(-1, "test_sensor_type")
        print(db)

# with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#     with conn.cursor() as cursor:
#         #cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
#         cursor.execute("SELECT * FROM dbo.SensorData")
#         row = cursor.fetchone()
#         while row:
#             #print (str(row[0]) + " " + str(row[1]))
#             print(row)
#             row = cursor.fetchone()

'''
------------------ CREATING DATA -------------
IF OBJECT_ID('[dbo].[SensorData]', 'U') IS NULL
CREATE TABLE [dbo].[SensorData]
(
    [Timestamp] INT NOT NULL, -- Primary Key column
    [SensorID] INT NOT NULL,
    [SensorType] TEXT NOT NULL,
    [Value] REAL NOT NULL,
    CONSTRAINT SensorData_pk PRIMARY KEY (Timestamp, SensorID)
    -- Specify more columns here
);
GO
-----------------------------------------------
------------------- INSERTING DATA -------------
INSERT INTO dbo.SensorData VALUES (121217, -1, 'test_sensor_type', -999);
'''
