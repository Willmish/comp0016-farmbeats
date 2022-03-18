from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv
from pubsub import pub
from datetime import datetime
import os
import tools.config

class IoTHubStreamer:
    sensor_data_topic = "actuator"
    MSG_TEXT = (
        '{{"Timestamp": {timestamp},'
        '"SensorID": {sensor_id},'
        '"SensorType": {sensor_type},'
        '"Value": {value},'
        '"ActuatorValue": {actuator_value}}}'
    )

    def __init__(self):
        load_dotenv()
        self._connection_string = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
        self._client = IoTHubDeviceClient.create_from_connection_string(
            self._connection_string
        )

    def __enter__(self):
        self._client.connect()
        pub.subscribe(
            self.sensor_data_listener, IoTHubStreamer.sensor_data_topic
        )
        return self

    def __exit__(self, type, value, traceback):
        self._client.shutdown()
        pub.unsubscribe(
            self.sensor_data_listener, IoTHubStreamer.sensor_data_topic
        )

    def sensor_data_listener(self, args):
        print("IoTHubStreamer: Received data over pubsub ", args)
        date = str(datetime.fromtimestamp(args.timestamp))
        msg_text_formatted = IoTHubStreamer.MSG_TEXT.format(
            timestamp='"' + date + '"',
            sensor_id=args.sensor_id,
            sensor_type='"' + args.sensor_type + '"',
            value=args.sensor_value,
            actuator_value=args.actuator_value,
        )
        message = Message(msg_text_formatted)
        self._client.send_message(message)


if __name__ == "__main__":
    # Test the IoTHub connection.
    import sys
    from time import time, sleep

    with IoTHubStreamer() as streamer:
        sys.path.insert(0, "..")
        from tools.sensor_data import SensorData

        while 1:
            pub.sendMessage(
                tools.config.actuator['actuator_value'],
                args=SensorData(time(), -1, "test_sensor_type", -999, 50),
            )
            sleep(5)
