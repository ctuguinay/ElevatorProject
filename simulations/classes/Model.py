from classes.Commands import Idle, OpenCloseDoors, Move, Command
from typing import Dict

class Model:
    """
    Attributes:
        if_ascending: either a boolean or None. True if the people in the elevator want
            to go up, False if they want to go down, None if there is nobody in the elevator
    """

    def __init__(self):
        self.if_ascending = None


    def get_command(self, curr_pos:int, buttons_pressed:Dict[int,bool], 
        up_buttons:Dict[int,bool], down_buttons:Dict[int,bool]) -> Command:
        """
        A command that will tell us the next thing to do, given information that
        is supposed to be provided to the elevator (in particular, the Model gets to know
        the current position, a list of buttons pressed within the elevator, the floor with hall
        calls going up, and the floor with hall calls going down)
        Args:
            curr_pos: current position of the elevator
            buttons_pressed: map from floor number to if the button for that floor in the elevator
                has been pressed or not
            up_buttons: map from floor number to if that floor has an upward hall call
            down_buttons: map from floor number to if that floor has a downward hall call
        """
        return Idle(None)