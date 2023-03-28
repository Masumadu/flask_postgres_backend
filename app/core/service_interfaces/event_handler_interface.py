import abc


class EventHandlerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "event_handler")) and callable(subclass.event_handler)

    @abc.abstractmethod
    def event_handler(self, event_data):
        """

        :param event_data: data publish as a result of event
        :return:
        """
        raise NotImplementedError
