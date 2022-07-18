try:
    from simulations.classes.Elevator import Elevator
except:
    from classes.Elevator import Elevator

class State(object):
    """
    Keeps track of the past, current, and result state of each increment of the simulation.

    Args:
        up_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the up button has been pressed on said floor.
        down_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the down button has been pressed on said floor.
        current_intended_destination: Integer for the floor where the elevator is currently trying to go to.
        time: Integer for time of the simulation in seconds.
        elevator: Elevator object which the simulation runs on.

    Attributes:
        up_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the up button has been pressed on said floor.
        down_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the down button has been pressed on said floor.
        current_intended_destination: Integer for the floor where the elevator is currently trying to go to.
        time: Integer for time of the simulation in seconds.
        elevator: Elevator object which the simulation runs on.
    """

    def __init__(self, up_calls, down_calls, current_intended_destination, time, elevator_speed, wait_time, elevator):
        """
        Initialize state object with the given parameters.
        """

        if (type(up_calls) is not dict):
            raise TypeError("The up_calls arg is not of type dictionary.")
        self.up_calls = up_calls

        if (type(down_calls) is not dict):
            raise TypeError("The down_calls arg is not of type dictionary.")
        self.down_calls = down_calls

        if (type(current_intended_destination) is not int):
            raise TypeError("The current_intended_destionation arg is not of type int.")
        self.current_intended_destination = current_intended_destination

        if (type(time) is not int):
            raise TypeError("The time arg is not of type int.")
        self.time = time

        if (type(elevator_speed) is not int):
            raise TypeError("The elevator_speed arg is not of type int")
        self.elevator_speed = elevator_speed


        if (type(wait_time) is not int):
            raise TypeError("The wait_time arg is not of type int")
        self.wait_time = wait_time

        if (type(elevator) is not Elevator):
            raise TypeError("The elevator arg is not of type Elevator.")
        self.elevator = elevator