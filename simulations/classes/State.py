class State(object):
    """
    Keeps track of the past, current, and result state of each increment of the simulation.

    Args:
        up_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the up button has been pressed on said floor.
        down_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the down button has been pressed on said floor.
        buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not (in the elevator).
        current_intended_destination: Integer for the floor where the elevator is currently trying to go to.
        current_location: Float for where the elevator currently is at.
        time: Integer for time of the simulation in seconds.

    Attributes:
        up_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the up button has been pressed on said floor.
        down_calls: Dictionary where the Keys is the number of a floor and the Values are booleans for whether the down button has been pressed on said floor.
        buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not (in the elevator).
        current_intended_destination: Integer for the floor where the elevator is currently trying to go to.
        current_location: Float for where the elevator currently is at.
        time: Integer for time of the simulation in seconds.
    """

    def __init__(self, up_calls, down_calls, buttons_pressed, current_intended_destination, current_location, time):
        """
        Initialize state object with the given parameters.
        """

        self.up_calls = up_calls
        self.down_calls = down_calls
        self.buttons_pressed = buttons_pressed
        self.current_intended_destination = current_intended_destination
        self.current_location = current_location
        self.time = time