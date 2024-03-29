"""
A file to store the classes that get passed into TimeListEvents, describing specific events

HallCalls are also used as elements of the lists that are the values in up_calls and down_calls in the State object.
"""

from typing import Union
try:
    from simulations.classes.ClassUtilities import validated
except:
    from classes.ClassUtilities import validated
from dataclasses import dataclass


@validated
@dataclass
class HallCall:
    """
    An object used to describe the event of an individual's hall call

    Args:
        time: the time the hall call was made
        person_id: the id of the person
        start_floor: the floor on which the hall call was made
        dest_floor: the floor that the caller wants to go to
        weight: weight of the person

    Attributes:
        time: the time the hall call was made
        person_id: the id of the person
        start_floor: the floor on which the hall call was made
        dest_floor: the floor that the caller wants to go to
        weight: weight of the person
    """
    person_id: int
    time: Union[int, float]
    start_floor: int
    dest_floor: int
    weight: float

    def __str__(self):
        return f"(person_id:{self.person_id}, start_floor:{self.start_floor}, dest_floor:{self.dest_floor}, weight:{self.weight})"

    def __repr__(self):
        return self.__str__()


@validated
@dataclass
class Arrival:
    """
    An object to be used in a TimeListEvent, used to describe the event of arriving at a floor
    Args:
        floor: the floor we're arriving at
    Attributes:
        floor: the floor we're arriving at
    """
    floor: int

class DoorClose:
    """
    An object to be used in a TimeListEvent, used to describe the elevator doors closing (ending a period
    of "letting people in")

    No attributes, no arguments
    """

    pass

class IdleEnd:
    """
    An object to be used in a TimeListEvent, used to describe the end of an "idle period".
    Used to ensure the TimeList doesn't run out of events before the end

    No attributes, no arguments.
    """
