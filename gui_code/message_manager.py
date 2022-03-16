
class MessageManager:
    def __init__(self, profile_name, status):
        self.message = ""
        self.get_message(profile_name, status)

    def get_message(self, profile_name, status):
        if status == 2:
            self.message = "Sensor reading seems good!"
        if profile_name == "Brightness":
            if status == 0:
                self.message = "Please increase LED brightness a lot more!"
            elif status == 1:
                self.message = "Please increase LED brightness a little."
            elif status == 3:
                self.message = "Please decrease LED brightness a little."
            elif status == 4:
                self.message = "Please decrease LED brightness a lot more!"
        elif profile_name == "Humidity":
            if status == 0:
                self.message = "Please decrease fan speed a lot more!"
            elif status == 1:
                self.message = "Please decrease fan speed a little."
            elif status == 3:
                self.message = "Please increase fan speed a little."
            elif status == 4:
                self.message = "Please increase fan speed a lot more!"
        elif profile_name == "Temperature":
            if status == 0:
                self.message = "Please increase heating a lot more!"
            elif status == 1:
                self.message = "Please increase heating a little."
            elif status == 3:
                self.message = "Please decrease heating a little."
            elif status == 4:
                self.message = "Please decrease heating a lot more!"
        elif profile_name == "Water Level":
            if status == 0:
                self.message = "Please add more water!"
            elif status == 1:
                self.message = "Please add a bit more water."
            elif status == 3:
                self.message = "No need to water. Moisture level is a little high."
            elif status == 4:
                self.message = "No need to water. Moisture level is very little high."