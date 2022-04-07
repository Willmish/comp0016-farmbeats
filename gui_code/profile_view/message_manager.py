from tools.constants import Constants


class MessageManager:
    def __init__(self, profile_name, status):
        """
        __init__ creates MessageManager object that will get
        an appropriate message corresponding with profile status.

        :param profile_name: Name of subsystem selected.
        :type profile_name: str
        :param status: Integer representing whether status
            is green, red or amber.
        :type status: int
        """
        self.message = ""

        if status == Constants.GREEN.value:
            self.message = "The sensor reading seems good!"
        elif status == Constants.NO_STATUS.value:
            self.message = "No current sensor reading."
        else:
            if profile_name == "Brightness":
                if status == Constants.RED_LOWER.value:
                    self.message = (
                        "Please increase the LED brightness a lot more!"
                    )
                elif status == Constants.AMBER_LOWER.value:
                    self.message = (
                        "Please increase the LED brightness a little."
                    )
                elif status == Constants.AMBER_UPPER.value:
                    self.message = (
                        "Please decrease the LED brightness a little."
                    )
                elif status == Constants.RED_UPPER.value:
                    self.message = (
                        "Please decrease the LED brightness a lot more!"
                    )
            elif profile_name == "Humidity":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please decrease the fan speed a lot more!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please decrease the fan speed a little."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = "Please increase the fan speed a little."
                elif status == Constants.RED_UPPER.value:
                    self.message = "Please increase the fan speed a lot more!"
            elif profile_name == "Temperature":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please increase the heating a lot more!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please increase the heating a little."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = "Please decrease the heating a little."
                elif status == Constants.RED_UPPER.value:
                    self.message = "Please decrease the heating a lot more!"
            elif profile_name == "Soil Moisture":
                if status == Constants.RED_LOWER.value:
                    self.message = "Please add more water!"
                elif status == Constants.AMBER_LOWER.value:
                    self.message = "Please add a bit more water."
                elif status == Constants.AMBER_UPPER.value:
                    self.message = (
                        "No need to water."
                        + "The moisture level is a little high."
                    )
                elif status == Constants.RED_UPPER.value:
                    self.message = (
                        "No need to water. The moisture level is very high."
                    )
