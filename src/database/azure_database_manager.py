from pubsub import pub
from database.database_manager import DatabaseManager
import pyodbc

import pyodbc
server = 'iot-farmbeats.database.windows.net'
database = 'iot-farmbeats'
username = 'iotFarmBeats2022'
password = '{plantGrowth22}'
driver= '{ODBC Driver 18 for SQL Server}'

class AzureDatabaseManager(DatabaseManager):
    ...

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        #cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        cursor.execute("SELECT * FROM dbo.SensorData")
        row = cursor.fetchone()
        while row:
            #print (str(row[0]) + " " + str(row[1]))
            print(row)
            row = cursor.fetchone()

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
