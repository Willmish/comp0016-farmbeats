from pubsub import pub
from typing import List


class Analyser:
    def __init__(self, sensor_type_topics: List[str],
                 actuator_type_topics: List[str], analyser_id: str):
        self._sensor_type_topics: List[str] = sensor_type_topics
        self._actuator_type_topics: List[str] = actuator_type_topics
        self._id = analyser_id
        for topic in self._sensor_type_topics:
            pub.subscribe(self.analyser_listener, topic)

    def analyser_listener(self, args, rest=None):
        pass
