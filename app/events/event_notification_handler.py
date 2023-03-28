from app.core import NotificationHandler
from app.producer import publish_to_kafka
from config import Config

from .event_data_structure import ServiceEventPublishing


class EventNotificationHandler(NotificationHandler):
    """
    Event Notification handler

    this class handles event notification. It publishes an Event message to
    the kafka broker which is consumed by the rightful service.

    :param publish: {enum} the event action to publish
    :param data: {object} the details of the event to be sent. based on
    the event details, a record may be altered in the rightful service.
    """

    def __init__(self, publish, data, schema=None):
        self.publish = publish
        self.service_name = Config.APP_NAME
        if schema:
            self.data = schema().dump(data)
        else:
            self.data = data

    def send(self):
        # validate the event data against a data structure
        if self.validate_event(self.data):
            publish_to_kafka(
                topic=self.publish.upper(), value=self.generate_event_data()
            )

    def validate_event(self, data):
        validator = ServiceEventPublishing[self.publish].value
        for field in validator:
            if field not in data:
                return None
            if isinstance(validator.get(field), list):
                if data.get(field) not in validator.get(field):
                    return None
        return data

    def generate_event_data(self):
        return {
            "service_name": self.service_name,
            "details": self.data,
            "meta": {
                "event_action": self.publish,
            },
        }
