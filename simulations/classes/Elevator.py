from dataclasses import dataclass
try:
    from simulations.classes.ClassUtilities import validated
except:
    from classes.ClassUtilities import validated



@validated
@dataclass
class Elevator(object):
    """
    Elevator object to help us keep track of elevator parameters and functionalities.

    Args:
        current_floor: Integer for the floor that the elevator starts at.
        top_floor: Integer for the highest floor that the elevator can visit.
        persons_in_elevator: Dictionary of all people in the elevator 
        where Keys are a person's ID (strings) and Values is an array with the person's destination floor as the
        0 index, the time they started waiting as the 1 index, and their weight as the 2 index.
        buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not.

    Attributes:
        current_floor: Integer for the floor that the elevator is currently at.
        top_floor: Integer for the top floor that the elevator can visit.
        persons_in_elevator: Dictionary of all people in the elevator 
        where Keys are a person's ID (strings) and Values are HallCalls
        capacity: The elevator's weight capacity
        curr_weight: The elevator's current weight
        moving: Boolean that is true if the elevator is moving (between floors), false otherwise.
        letting_people_in: Boolean that is true if the elevator is in the process of letting people in, false otherwise.
        buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not.
        going_up: True if the elevator's doors are open and the elevator intends to go up, False if the doors are
        open and it intends to go down, None if the doors are not open
    """

    current_floor: int
    top_floor: int
    capacity: float
    persons_in_elevator: dict
    buttons_pressed: dict

    def __post_init__(self):
        """
        Sets other fields of the Elevator object.
        """       
        self.moving = False
        self.letting_people_in = False
        self.going_up = None
        self.curr_weight = 0


    def add_floor(self, calls:dict) -> None:
        """
        Adds the current floor of passengers to the elevator (in either the up or down direction). 
        We are assuming it takes 0 seconds to load a passenger.

        Args: 
            calls: either the up or down calls array, depending on which array of people are being added

        Returns:
            number_people: Int for the number of people added to the elevator.
        """

        waiting = calls[self.current_floor]
        number_people = 0
        for person in waiting:
            if self.curr_weight + person.weight < self.capacity:
                self.persons_in_elevator[self.current_floor].append(person)
                calls[self.current_floor].remove(person)
                self.button_pressed(person.dest_floor)
                self.curr_weight += person.weight
                number_people =+ 1
            else:
                # no more room
                break
        
        return number_people

    def button_pressed(self, button_pressed):
        """
        Updates the buttons that were pressed.

        Args:
            button_pressed: Integer corresponding to the button that was pressed.
            
        Returns:
            button_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not.
        """

        if button_pressed > self.top_floor or button_pressed < 1:
            raise TypeError("Target floor " + str(button_pressed) + " is not in range of floors.")

        self.buttons_pressed[button_pressed] = True
        return self.buttons_pressed
        
    def total_passenger_weight(self) -> int:
        """
        Returns the total weight of all passengers in the elevator
        """
        res = 0
        for floor_list in self.persons_in_elevator.values():
            for person in floor_list:
                res += person.weight
        
        return res