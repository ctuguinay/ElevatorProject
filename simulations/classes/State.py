try:
    from simulations.classes.Elevator import Elevator
except:
    from classes.Elevator import Elevator
from dataclasses import dataclass
from typing import Union
from simulations.classes.ClassUtilities import validated

@validated
@dataclass
class State(object):
    """
    Keeps track of the past, current, and result state of each increment of the simulation.

    Args:
        up_calls: Dictionary where the Keys is the number of a floor and the Values are lists of HallCalls representing people that pressed the up button on the floor.
        down_calls: Dictionary where the Keys is the number of a floor and the Values are lists of HallCalls representing people that pressed the down button on the floor.
        current_intended_destination: Integer for the floor where the elevator is currently trying to go to. None if the elevator
            doesn't intend to go anywhere.
        time: Integer for time of the simulation in seconds.
        elevator_speed: Integer for the speed of all elevators in "seconds per traversal of single floor"
        wait_time: Integer for the time an elevator waits on each floor for people to get in. This represents the physical processes
            of opening the door, waiting for people to enter, and closing the door
        elevator: Elevator object which the simulation runs on.

    Attributes:
        up_calls: Dictionary where the Keys is the number of a floor and the Values are lists of HallCalls representing people that pressed the up button on the floor.
        down_calls: Dictionary where the Keys is the number of a floor and the Values are lists of HallCalls representing people that pressed the down button on the floor.
        current_intended_destination: Integer for the floor where the elevator is currently trying to go to. None if the elevator
            doesn't intend to go anywhere.
        time: Integer for time of the simulation in seconds.
        elevator_speed: Integer for the speed of all elevators in "seconds per traversal of single floor"
        wait_time: Integer for the time an elevator waits on each floor for people to get in. This represents the physical processes
            of opening the door, waiting for people to enter, and closing the door
        elevator: Elevator object which the simulation runs on.
    """

    up_calls: dict
    down_calls: dict
    time: int
    elevator_speed: int
    wait_time: int
    elevator: Elevator
