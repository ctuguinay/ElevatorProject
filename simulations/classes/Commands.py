"""
A list of commands that a model or algorithm can give to the elevator
"""

class Command():
    """
    Generic subclass for commands
    """
    """
    Args:
        intended_destination: the new intended destination for the elevator
    Attributes:
        intended_destination: the new intended destination for the elevator
    """

    def __init__(self, intended_destination):
        if (type(intended_destination) is not int and intended_destination is not None):
            raise TypeError("The intended_destination arg is neither None nor of type int.")
        self.intended_destination = intended_destination

class Idle(Command):
    """
    A Command that tells the elevator to idle
    Args:
        intended_destination: the new intended destination for the elevator
    Attributes:
        Only those from superclass
    """
    def __init__(self, intended_destination):
        super().__init__(intended_destination)


class OpenCloseDoors(Command):
    """
    A Command that asks the elevator to undergo the process of letting people in
    Args:
        intended_destination: the new intended destination for the elevator
    Attributes:
        Only those from superclass
    """
    def __init__(self, intended_destination):
        super().__init__(intended_destination)

class Move(Command):
    """
    A Command that asks the elevator to either move up one floor or down one floor
    Args:
        if_up: True if the elevator is being asked to move up, false if down
        intended_destination: the new intended destination for the elevator
    Attributes:
        Attributes from superclass Command()
        if_up: True if the elevator is being asked to move up, false if down
    """


    def __init__(self, inteneded_destination, if_up):
        if (type(if_up) is not bool):
            raise TypeError("Argument if_up is not of type bool")
        super().__init__(inteneded_destination)
        self.if_up = if_up