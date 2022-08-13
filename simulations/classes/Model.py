try:
    from simulations.classes.Commands import Idle, OpenCloseDoors, Move, Command
except:
    from classes.Commands import Idle, OpenCloseDoors, Move, Command
import numpy as np
from typing import Dict
from enum import Enum

class HallCallStatus(Enum):
    """
    One of four possible statuses relating the elevator's current
    position to the state of hall calls in the building.
    """
    NONE = 1 # no hall calls
    CLOSEST_UP = 2 # after uniformly randomly choosing between the closest floors, the chosen floor is up
    CLOSEST_DOWN = 3 # after uniformly randomly choosing between the closest floors, the chosen floor is down
    CLOSEST_HERE = 4 # there's a hall call on this floor


class Model:
    """
    Description of the Algorithm:
        In the beginning, the elevator either Idles if no hall calls are requested, or otherwise Moves
        towards one of the closest floors (chosen uniformly randomly) in which a hall call was requested. When the
        elevator reaches a floor in which a hall call is made, it issues an OpenCloseDoors where the
        intended direction is uniformly randomly chosen between one of the directions in which
        a hall call is requested at the floor. When passengers get in, the elevator ferries all passengers
        to their desired destination, either going up or down. While this is happening, if the elevator 
        passes floors with Hall Calls in its intended direction, it issues an OpenCloseDoors and lets 
        more passengers in. This process will eventually end when the elevator is empty, in which case
        the elevator will again either Idle or search for one of the closest floors to again start
        transporting passengers.
    """

    def __init__(self):
        pass

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
        if_relative_buttons_up = None
        for floor,pressed in buttons_pressed.items():
            # all buttons pressed other than the current floor should be above
            # or below the current level
            if floor != curr_pos and pressed:
                if floor < curr_pos:
                    if_relative_buttons_up = False
                else:
                    if_relative_buttons_up = True
        
        if buttons_pressed[curr_pos]:
            # this button is pressed, we must let people off
            if if_relative_buttons_up is not None:
                # some other buttons are pressed, we should keep
                # travelling in that direction
                return OpenCloseDoors(going_up=if_relative_buttons_up)
            else:
                # no other buttons are pressed, we must decide a new
                # direction to travel in
                hall_call_status = self._if_closest_floor_up(curr_pos,up_buttons,down_buttons)
                if hall_call_status == HallCallStatus.NONE:
                    # no other hall calls made, the direction is arbitrary
                    return OpenCloseDoors(going_up=True)
                # otherwise, pick the direction that HallCallStatus tells us to go in
                elif hall_call_status == HallCallStatus.CLOSEST_UP:
                    return OpenCloseDoors(going_up=True)
                elif hall_call_status == HallCallStatus.CLOSEST_DOWN:
                    return OpenCloseDoors(going_up=False)
                elif hall_call_status == HallCallStatus.CLOSEST_HERE:
                    direction_intention = self._if_hall_call_up(curr_pos,up_buttons,down_buttons)
                    if direction_intention is None:
                        raise RuntimeError("_if_closest_floor_up yields that there are hall calls on this floor,"\
                            +"but _if_hall_call_up yields that there are none")
                    return OpenCloseDoors(direction_intention)
                else:
                    raise ValueError("Unexpected return from _if_closest_floor_up")
        
        if if_relative_buttons_up is not None:
            # this button isn't pressed, but some buttons are. Keep travelling in those buttons' direction
            return Move(if_up=if_relative_buttons_up)


        # No buttons are pressed at all, no passengers are in the elevator
        hall_call_status = self._if_closest_floor_up(curr_pos,up_buttons,down_buttons)
        if hall_call_status == HallCallStatus.NONE:
            return Idle() # No passengers, no hall calls
        elif hall_call_status == HallCallStatus.CLOSEST_UP:
            return Move(if_up=True)
        elif hall_call_status == HallCallStatus.CLOSEST_DOWN:
            return Move(if_up=False)
        elif hall_call_status == HallCallStatus.CLOSEST_HERE:
            direction_intention = self._if_hall_call_up(curr_pos,up_buttons,down_buttons)
            if direction_intention is None:
                raise RuntimeError("_closest_floor yields that there are hall calls on this floor,"\
                    +"but _if_hall_call_up yields that there are none")
            return OpenCloseDoors(direction_intention)
        else:
            raise ValueError("Unexpected return from _closest_floor")
                
    
    def _if_closest_floor_up(self,curr_pos:int, up_buttons:Dict[int,bool], 
        down_buttons:Dict[int,bool]) -> HallCallStatus:
        """
            Args:
                curr_pos: the current position of the elevator
                up_buttons: map from floor number to if that floor has an upward hall call
                down_buttons: map from floor number to if that floor has a downward hall call
            Utility function that assumes the elevator's current floor has no Hall Calls.
            Returns the Status that fits the situation
        """
        min_dist = None
        closest_floors = []
        for floor in up_buttons:
            if up_buttons[floor] or down_buttons[floor]:
                dist = np.abs(floor-curr_pos)
                if dist == 0:
                    return HallCallStatus.CLOSEST_HERE
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    closest_floors = [floor]
                elif min_dist == dist:
                    closest_floors.append(floor)
        if min_dist is None:
            return HallCallStatus.NONE
        chosen_floor = np.random.choice(closest_floors)
        if chosen_floor > curr_pos:
            return HallCallStatus.CLOSEST_UP
        return HallCallStatus.CLOSEST_DOWN
    
    def _if_hall_call_up(self,curr_pos:int, up_buttons:Dict[int,bool], 
        down_buttons:Dict[int,bool]):
        """
            Args:
                curr_pos: the current position of the elevator
                up_buttons: map from floor number to if that floor has an upward hall call
                down_buttons: map from floor number to if that floor has a downward hall call
            Utility function for uniformly randomly choosing a direction
            in which a hall call has been made on the elevator's current floor.
            Returns True if the direction is up, False if down, None if no hall
            calls have been made on the current floor
        """
        choices = []
        if up_buttons[curr_pos]:
            choices.append(True)
        if down_buttons[curr_pos]:
            choices.append(False)
        if choices == []:
            return None
        else:
            return np.random.choice(choices)
