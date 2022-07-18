"""
A file to store the classes that get passed into TimeListEvents, describing specific events

HallCalls are also used as elements of the lists that are the values in up_calls and down_calls in the State object.
"""

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

    def __init__(self, person_id, time, start_floor, dest_floor, weight):
        if (type(time) is not int and type(time) is not float):
            raise TypeError("The argument time is not numeric")
        self.time = time

        if (type(person_id) is not int):
            raise TypeError("The argument person_id is not of type int")
        self.person_id = person_id

        if (type(start_floor) is not int):
            raise TypeError("The argument start_floor is not of type int")
        self.start_floor = start_floor

        if (type(dest_floor) is not int):
            raise TypeError("The argument dest_floor is not of type int")
        self.dest_floor = dest_floor

        if (type(weight) is not float):
            raise TypeError("The argument weight is not of type float")
        self.weight = weight
    
    def __str__(self):
        return f"(person_id:{self.person_id}, start_floor:{self.start_floor}, dest_floor:{self.dest_floor}, weight:{self.weight})"

    def __repr__(self):
        return self.__str__(self)

class Arrival:
    """
    An object to be used in a TimeListEvent, used to describe the event of arriving at a floor
    Args:
        floor: the floor we're arriving at
    Attributes:
        floor: the floor we're arriving at
    """
    def __init__(self, floor):
        if (type(floor) is not int):
            raise TypeError("The argument floor is not of type int")
        self.floor = floor

class DoorClose:
    """
    An object to be used in a TimeListEvent, used to describe the elevator doors closing (ending a period
    of "letting people in")

    No attributes, no arguments
    """

    pass
