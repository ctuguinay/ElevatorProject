class TimeListEvent(object):
    """
    Keeps track of the information in an event in the simulation.

    Args:
        time: Integer for the time of the simulation in seconds.
        object_type: String describing event type.
        object: Object storing information about event.

    Attributes:
        time: Integer for the time of the simulation in seconds.
        object_type: String describing event type.
        object: Object storing information about event.
    """

    def __init__(self, time, object_type, object):
        """
        Initialize timelist event object with the given parameters.
        """
        
        if (type(time) is not int):
            raise TypeError("The time arg is not of type int.")
        self.time = time

        if (type(object_type) is not str):
            raise TypeError("The object_type arg is not of type string.")
        self.object_type = object_type

        self.object = object

class TimeList(object):
    """
    Keeps track of the current and future events that will happen in the simulation.

    Attributes:
        future: Array of TimeListEvents that are yet to happen.
        past: Array of TimeListEvents that have happened.
    """

    def __init__(self):
        """
        Initialize timelist object with the given parameters.
        """

        self.future = []
        self.past = []

    def next_event(self):
        """
        Gets the next timelist event and reorganizes both lists.

        Returns:
            current_event: Timelist event that is designated as the most current event on the future list.
        """

        current_event = self.future[0]
        self.future = self.future[1:]
        self.past.append(current_event)
        return current_event

    def add_event(self, input_event):
        """
        Adds an event to the futures list.

        Args:
            input_event: Event to be placed into the future list.
        """

        if (type(input_event) is not TimeListEvent):
            raise TypeError("The input_event arg is not of type TimeListEvent.")

        if len(self.future) != 0:
            inserted = False
            input_event_time = input_event.time
            for index, event in enumerate(self.future):
                if event.time > input_event_time:
                    self.future.insert(index, input_event)
                    inserted = True
                    break
            if not inserted:
                self.future.append(input_event)
        else:
            self.future = [input_event]

    def has_next(self):
        """
        Tells whether or not there are still events left in the future list.

        Returns:
            has_next_value: Boolean for whether or not there are still events left in the future list.
        """

        if len(self.future) == 0:
            has_next_value = False
        else:
            has_next_value = True

        return has_next_value