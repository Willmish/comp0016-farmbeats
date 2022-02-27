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
            "FROM dbo.SensorData b WHERE b.SensorType = '" + 
            subsys_name +"') AND a.SensorType = '" + subsys_name + "';"
            
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
        return curr_vals

    def get_time_and_val_list(self, subsys_name):
        vals = []
        times = []

        for row in self._cursor.execute(
            '''
            SELECT  Value, Timestamp
            FROM dbo.SensorData ''' +
            "WHERE SensorType = '" + subsys_name + "';"
            
        ):
            vals.append(row[0])
            times.append(row[1])

        return (vals, times)
    
    def get_val_list(self, subsys_name):
        values = []

        for row in self._cursor.execute(
            '''
            SELECT  Value
            FROM dbo.SensorData ''' +
            "WHERE SensorType = '" + subsys_name + "';"
            
        ):
            values.append(row[0])
        return values

    def __repr__(self) -> str:
        res = ''
        for row in self._cursor.execute("SELECT * FROM dbo.SensorData;"):
            res += str(row) + '\n'
        return res


    