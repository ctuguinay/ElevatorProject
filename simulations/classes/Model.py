from classes.Commands import Idle, OpenCloseDoors, Move

class Model:
    def get_command(state):
        """
        A command that will tell us the next thing to do, given the current state. 
        Args:
            state: the current state
        """
        return Idle(None)