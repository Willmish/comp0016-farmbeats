from tools.constants import Constants

class MessageManager:
    def __init__(self, profile_name, status):
        """
        __init__ creates MessageManager object that will get
        an appropriate message corresponding with the status.

        :param profile_name:
        :type profile_name: Str
        :param status:
        :type status: Int
        """
        self.message = ""
        
        if status == Constants.GREEN.value:
            self.message = "Sensor reading seems good!"
        elif status == Constants.NO_STATUS.value:
            self.message = "No current sensor reading."
        else:
            if profile_name == "Brightness":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please increase LED brightness a lot more!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please increase LED brightness a little."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = "Please decrease LED brightness a little."
                elif status == Constants.RED_UPPER.value:
                    self.message = "Please decrease LED brightness a lot more!"
            elif profile_name == "Humidity":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please decrease fan speed a lot more!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please decrease fan speed a little."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = "Please increase fan speed a little."
                elif status == Constants.RED_UPPER.value:
                    self.message = "Please increase fan speed a lot more!"
            elif profile_name == "Temperature":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please increase heating a lot more!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please increase heating a little."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = "Please decrease heating a little."
                elif status == Constants.RED_UPPER.value:
                    self.message = "Please decrease heating a lot more!"
            elif profile_name == "Water Level":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please add more water!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please add a bit more water."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = (
                        "No need to water. Moisture level is a little high."
                    )
                elif status == Constants.RED_UPPER.value:
                    self.message = (
                        "No need to water. Moisture level is very little high."
                    )
