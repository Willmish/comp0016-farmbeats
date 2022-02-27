from pubsub import pub
from database_manager import DatabaseManager
import pyodbc


server = 'iot-farmbeats.database.windows.net'
database = 'iot-farmbeats'
username = 'iotFarmBeats2022'
password = '{plantGrowth22}'
driver = '{ODBC Driver 18 for SQL Server}'


class GuiDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__('azure_db')
    
    def __enter__(self):
        self._azure_conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
        self._cursor = self._azure_conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self._azure_conn.close()
    
    def get_curr_val_single_subsys(self, subsys_name):
        total = 0
        count = 0
        for row in self._cursor.execute(
            '''
            SELECT  Value
            FROM dbo.SensorData a 
            WHERE Timestamp = (SELECT MAX(Timestamp) ''' +
            "FROM dbo.SensorData b WHERE b.SensorType = '" + subsys_name +"') AND a.SensorType = '" + subsys_name + "';"
            
        ):
            
            total += row[0]
            count +=1
        return total/count

    def collect_curr_val(self):
        #[brightness, humidity, temperature, water]
        curr_vals = [
            self.get_curr_val_single_subsys('brightness'),
            self.get_curr_val_single_subsys('humidity'),
            self.get_curr_val_single_subsys('temperature'),
            self.get_curr_val_single_subsys('water level')
            ] 
        print (curr_vals)
        return curr_vals

    def __repr__(self) -> str:
        res = ''
        for row in self._cursor.execute("SELECT * FROM dbo.SensorData;"):
            res += str(row) + '\n'
        return res

import sys
sys.path.insert(0, '..')
with GuiDatabaseManager() as db:
    db.collect_curr_val()

    