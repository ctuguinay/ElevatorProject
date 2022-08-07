from dataclasses import dataclass
try:
    from simulations.classes.ClassUtilities import validated
    from simulations.classes.State import State
    from simulations.classes.TimeList import TimeList
except:
    from classes.ClassUtilities import validated
    from classes.State import State
    from classes.TimeList import TimeList

@validated
@dataclass
class LogPIT(object):
    """
    Keeps track of all the information in the simulation at a single point in time, for later use.
    Different from TimeList event object.

    Args:
        result_state: The result state after using useState.
        timelist: Current timelist in simulation.
        added_time: Current added_time in simulation.
        total_time: Current total_time in simulation.

    Attributes:
        result_state: The result state after using useState.
        timelist: Current timelist in simulation.
        added_time: Current added_time in simulation.
        total_time: Current total_time in simulation.
    """

    result_state: State
    timelist: TimeList
    added_time: list
    total_time: list


class Log(object):
    """
    Keeps track of all the information in the simulation at all relevant points in time, for later use.
    Different from TimeList object.

    Attributes:
        log_pit_list: Array containing all Log PIT objects.
        pointer: pointing at the 
    """

    def __init__(self):
        """
        Initialize timelist object with the given parameters.
        """

        self.log_pit_list = []
        self.pointer = 0

    def next_log_pit(self):
        """
        Gets the current Log PIT object and moves the pointer up by one.

        Returns:
            current_log_pit: The log pit event that the cursor is point at..
        """

        if (self.pointer + 1 > len(self.log_pit_list)):
            return None
        else:
            current_log_pit = self.log_pit_list[self.pointer]
            current_pointer = self.pointer
            self.pointer = current_pointer + 1
            return current_log_pit

    def add_log_pit(self, input_log_pit):
        """
        Adds an event to the futures list.

        Args:
            input_event: Event to be placed into the future list.
        """

        if (type(input_log_pit) is not LogPIT):
            raise TypeError("The input_event arg is not of type LogPIT.")
        if len(self.log_pit_list) == 0:
            self.log_pit_list = [input_log_pit]
        else:
            self.log_pit_list.append(input_log_pit)

    def length(self):
        """
        Returns length of log_pit list.
        """

        return len(self.log_pit_list)

    def return_pointer(self):
        """
        Returns current pointer.
        """

        return self.pointer

    def change_pointer(self, new_pointer):
        """
        Changes the pointer.

        Args:
            new_pointer: Changes the current pointer of the Log object, if it is in the correct range .
        """

        if (new_pointer not in range(len(self.log_pit_list) + 1)):
            raise ValueError("The new pointer arg is not within the range of log_pit_list.")

        self.pointer = new_pointer