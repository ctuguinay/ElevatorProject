from classes.Commands import Idle, OpenCloseDoors, Move

class Model:
    """
    Attributes:
        if_ascending: either a boolean or None. True if the people in the elevator want
            to go up, False if they want to go down, None if there is nobody in the elevator
    """

    def __init__(self):
        self.if_ascending = None


    def get_command(self, state):
        """
        A command that will tell us the next thing to do, given the current state. 
        Args:
            state: the current state
        """
        return Idle(None)