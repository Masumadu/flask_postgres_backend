import enum


class ServiceEventSubscription(enum.Enum):
    """

    This class defines all events subscribed by this service. Events are created in the
    form: event_name = {data_field: value_of_interest}.Above each event list
    various services publishing such event. Check out the respective service
    for more info concerning each event.

    """

    # nova-be-inventory
    cust_deposit = ["customer_id", "type_id"]


class ServiceEventPublishing(enum.Enum):
    """

    This class defines all events to be published by this service. Events are created in
    the form: event_name = {data_field: value_of_interest}. Above each event list
    various services subscribing to such event. Check out the respective service
     for more info concerning each event

    """


def extract_valid_data(obj_data: dict, validator: dict):
    valid_data = dict()
    for field in validator:
        valid_data[field] = obj_data.get(field)
    return valid_data
