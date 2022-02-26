from pubsub import pub
from database.database_manager import DatabaseManager
import pyodbc


server = 'iot-farmbeats.database.windows.net'
database = 'iot-farmbeats'
username = 'iotFarmBeats2022'
password = '{plantGrowth22}'
driver = '{FreeTDS}'


class GuiDatabaseManager:
    def __init__(self):
        super().__init__('azure_db')
    
    def __enter__(self):
        self._azure_conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
        self._cursor =  self._azure_conn.cursor()
        return self

    def __exit__(self):
        self._connection.close()
    
    def collect_curr_val(self) -> str:
        #[brightness, humidity, temperature, water]
        curr_vals = []
        for row in self._cursor.execute("SELECT Value FROM SensorData WHERE SensorType = brightness;"):
            print (row)
        return ''
    