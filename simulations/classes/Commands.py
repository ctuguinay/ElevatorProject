"""
A list of commands that a model or algorithm can give to the elevator
"""

from typing import Union
from dataclasses import dataclass
try:
    from simulations.classes.ClassUtilities import validated
except:
    from classes.ClassUtilities import validated


@validated
@dataclass
class Command():
    """
    Generic subclass for commands
    """


class Idle(Command):
    """
    A Command that tells the elevator to idle
    Args:
        intended_destination: the new intended destination for the elevator
    Attributes:
        Only those from superclass
    """
    def __init__(self):
        pass

    def __str__(self):
        return f"Idle: {{}}"
    
    def __repr__(self):
        return self.__str__()


class OpenCloseDoors(Command):
    """
    A Command that asks the elevator to undergo the process of letting people in
    Args:
        going_up: True if the elevator intends on taking people up, false otherwise
    Attributes:
        going_up: True if the elevator intends on taking people up, false otherwise
    """
    def __init__(self, going_up):
        self.going_up = going_up
    
    def __str__(self):
        return f"OpenCloseDoors: {{going_up: {self.going_up}}}"
    
    def __repr__(self):
        return self.__str__()

class Move(Command):
    """
    A Command that asks the elevator to either move up one floor or down one floor
    Args:
        if_up: True if the elevator is being asked to move up, false if down
    Attributes:
        if_up: True if the elevator is being asked to move up, false if down
    """


    def __init__(self, if_up):
        if (type(if_up) is not bool):
            raise TypeError("Argument if_up is not of type bool")
        self.if_up = if_up
    
    def __str__(self):
        return f"Move: {{if_up: {self.if_up}}}"
    
    def __repr__(self):
        return self.__str__()