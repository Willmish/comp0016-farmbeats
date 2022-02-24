from pubsub import pub
import pyodbc


server = 'iot-farmbeats.database.windows.net'
database = 'iot-farmbeats'
username = 'iotFarmBeats2022'
password = '{plantGrowth22}'
driver = '{ODBC Driver 18 for SQL Server}'


with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        #cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        cursor.execute("SELECT * FROM dbo.SensorData")
        row = cursor.fetchone()
        while row:
            #print (str(row[0]) + " " + str(row[1]))
            print(row)
            row = cursor.fetchone()