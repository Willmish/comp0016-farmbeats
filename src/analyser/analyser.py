from pubsub import pub
from typing import List
import tools.config as config


class Analyser:
    def __init__(
        self,
        sensor_type_topics: List[str],
        actuator_type_topics: List[str] = [],
        analyser_id: str = "",
    ):
        self._sensor_type_topics: List[str] = sensor_type_topics
        self._actuator_type_topics: List[str] = actuator_type_topics
        self._id = analyser_id
        for topic in self._sensor_type_topics:
            pub.subscribe(
                self.datastream_update_listener, config.database_update +"." + topic
            )
            pub.subscribe(self.analyser_listener, config.pid_update + "." + topic)

    def analyser_listener(self, args, rest=None):
        pass

    def datastream_update_listener(self, args, rest=None):
        pass
