from pubsub import pub
from signal import signal, alarm, SIGALRM, SIGKILL
from tools.logging import logDebug, logInfo
from tools.sensor_data import SensorData

class SignalHandler:
    MAIN_LISTEN_TOPIC = "pid_update"
    """
    Handles asynchrounous signals and calls the signal handler function.
    Uses pubsub to receive pump control messages from moisture_analyser module,
    then sends out pubsub messages to the actuator module. Afterwards, sets the alarm to
    which is handled by the signal handler function and turns off the pump after the alarm is triggered. 
    
    Pubsub SignalHandler message structure:
    Main Topic: "signal_handler"
    Pump control subtopics: "pump_control"
    Pump control message contents: {"signal_handler_message": {"pump_status": boolean, "time_on": int}, "messsage": SensorData}

    :return: _description_
    :rtype: _type_
    """
    # Initialise signal handler and basic signal handling functions
    def __init__(self):
        self.signal_received: bool = False
        self.pump_status: bool = False
        signal(SIGALRM, self.handler)
        pub.subscribe(self.pump_status_listener, "signal_handler.pump_control")

    # Signal handler  function
    def handler(self, signum, frame):
        self.signal_received = True
        if signum == SIGALRM:
            logDebug("Alarm triggered!")
            if self.pump_status:
                self.pump_status = False
                pub.sendMessage(f"{SignalHandler.MAIN_LISTEN_TOPIC}.actuator.water_pump_status", args=SensorData(actuator_value = 0.0))


    # Set alarm for a given time
    def set_alarm(self, time):
        alarm(time)
    
    def pump_status_listener(self, signal_handler_message, message):
        logInfo("Received pump vals over pubsub:", signal_handler_message)
        self.pump_status: bool = signal_handler_message["pump_status"]
        sensor_data: SensorData = message
        if self.pump_status:
            self.time_on = signal_handler_message["time_on"]
            pub.sendMessage(f"{SignalHandler.MAIN_LISTEN_TOPIC}.actuator.water_pump_status", args=sensor_data)
        self.set_alarm(self.time_on)


    # Check if signal was received
    def check_signal(self):
        return self.signal_received
    
    # Reset signal received
    def reset_signal(self):
        self.signal_received = False

    # Set signal received
    def set_signal(self):
        self.signal_received = True