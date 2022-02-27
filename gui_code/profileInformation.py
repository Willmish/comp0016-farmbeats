
from gui_database_manager import GuiDatabaseManager

INPUT = 800
LOWER = 700
UPPER = 850
EXLOWER = 600
EXUPPER = 950
ACTUATION = 900
MESSAGE = "The sensor readings seem good!"
LOWER_BOUND = 0
UPPER_BOUND = 1000
TIMELIST = [0,5,10,15,20,25,30,35,40,45]
VALUELIST = [904,920, 911, 890, 883,880,881, 860, 872, 888]

class ProfileInformation:
    def __init__(self, profileName):
        with GuiDatabaseManager() as db:
            self.title = profileName
            if profileName == "Brightness":
                self.sensorFrameTitle = "Light Sensor Information"
                self.sensorValue = db.get_curr_val_single_subsys('brightness')
                self.unit = "cd"
                self.sensorValueDescription = "Current value: " + str(self.sensorValue) + self.unit 

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.timeList = db.get_time_list('brightness')
                self.valList = db.get_val_list('brightness')
                self.graphTitle = "Brightness over Time"

                self.actuatorFrameTitle = "LED light Information"
                self.actuatorValue = ACTUATION
                self.actuatorValueDescription = "Brightness set to: "+ str(self.actuatorValue) + self.unit

                self.suggestion = MESSAGE

            elif profileName == "Humidity":
                self.sensorFrameTitle = "DH11 Sensor Information"
                self.sensorValue = db.get_curr_val_single_subsys('humidity')
                self.unit = "%"
                self.sensorValueDescription = "Current value: " + str(self.sensorValue) + self.unit 

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.timeList = db.get_time_and_val_list('humidity')[1]
                self.valList = db.get_time_and_val_list('humidity')[0]
                self.graphTitle = "Humidity over Time"

                self.actuatorFrameTitle = "Fan Information"
                self.actuatorValue = ACTUATION
                self.actuatorValueDescription = "Input speed set to: "+ str(self.actuatorValue) + self.unit + "\n Output speed set to: "+ str(self.actuatorValue) + self.unit

                self.suggestion = MESSAGE

            elif profileName == "Temperature":
                self.sensorFrameTitle = "DH11 Sensor Information"
                self.sensorValue = db.get_curr_val_single_subsys('temperature')
                self.unit = "°c"
                self.sensorValueDescription = "Current value: " + str(self.sensorValue) + self.unit 

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.timeList = db.get_time_and_val_list('temperature')[1]
                self.valList = db.get_time_and_val_list('temperature')[0]
                self.graphTitle = "Temperature over Time"

                self.actuatorFrameTitle = "Heater Information"
                self.actuatorValue = ACTUATION
                self.actuatorValueDescription = "Heater set to: "+ str(self.actuatorValue) + self.unit

                self.suggestion = MESSAGE
            elif profileName == "Water":
                self.sensorFrameTitle = "Soil moisture Sensor Information"
                self.sensorValue = db.get_curr_val_single_subsys('water level')
                self.unit = "%"
                self.sensorValueDescription = "Current value: " + str(self.sensorValue) + self.unit 

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.timeList = db.get_time_and_val_list('water level')[1]
                self.valList = db.get_time_and_val_list('water level')[0]
                self.graphTitle = "Soil Moisture over Time"

                self.actuatorFrameTitle = "Sprinkler Information"
                self.actuatorValue = ACTUATION
                self.actuatorValueDescription = "Amount of water added: "+ str(self.actuatorValue) + self.unit

                self.suggestion = MESSAGE

