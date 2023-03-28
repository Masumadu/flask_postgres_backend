from flask import current_app

from app.core.service_interfaces import EventHandlerInterface

from .event_data_structure import ServiceEventSubscription


class EventSubscriptionHandler(EventHandlerInterface):
    def __init__(self, customer_controller):
        self.customer_controller = customer_controller
        self.data = None
        self.details = None
        self.meta = None
        self.event_action = None

    def event_handler(self, event_data: dict):
        self.data = event_data
        self.details = event_data.get("details")
        self.meta = event_data.get("meta")
        self.event_action = self.meta.get("event_action")

        # reminder: validate event data against a pre-define data structure
        valid_event_data = self.validate_event(self.details)
        if valid_event_data:
            getattr(self, self.event_action, self.unhandled_event)()
        else:
            current_app.logger.critical(
                f"event {self.event_action} with data {self.data} did not pass data validation"  # noqa
            )

    def validate_event(self, data):
        if self.event_action in ServiceEventSubscription.__members__:
            validator = ServiceEventSubscription[self.event_action].value
            for field in validator:
                if field not in data:
                    return None
            return data
        return None

    def unhandled_event(self):
        current_app.logger.critical(
            f"event {self.event_action} with data {self.data} is unhandled"
        )

    def cust_deposit(self):
        """

        This event update's the attribute <level> on a customer to the size of
        cylinder deposited during first purchase. Event is published to the kafka
        topic <FIRST_TIME_DEPOSIT> by the Inventory Service to be consumed by this
        service.
        :return: None

        """
        self.customer_controller.cust_deposit(self.details)
