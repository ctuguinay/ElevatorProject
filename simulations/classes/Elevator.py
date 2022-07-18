class Elevator(object):
    """
    Elevator object to help us keep track of elevator parameters and functionalities.

    Args:
        start_floor: Integer for the floor that the elevator starts at.
        top_floor: Integer for the highest floor that the elevator can visit.
        persons_dictionary: Dictionary of all people in the elevator 
        where Keys are a person's ID (strings) and Values is an array with the person's destination floor as the
        0 index, the time they started waiting as the 1 index, and their weight as the 2 index.
        buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not.

    Attributes:
        current_floor: Integer for the floor that the elevator is currently at.
        top_floor: Integer for the top floor that the elevator can visit.
        persons_in_elevator: Dictionary of all people in the elevator 
        where Keys are a person's ID (strings) and Values is an array with the person's destination floor as the
        0 index, the time they started waiting as the 1 index, and their weight as the 2 index.
        moving: Boolean that is true if the elevator is moving (between floors), false otherwise.
        letting_people_in: Boolean that is true if the elevator is in the process of letting people in, false otherwise.
        buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not.
    """

    def __init__(self, start_floor, top_floor, persons_dictionary, buttons_pressed):
        """
        Initialize elevator object with the given parameters.
        """

        if (type(start_floor) is not int):
            raise TypeError("The start_floor arg is not of type int.")
        self.current_floor = start_floor

        if (type(top_floor) is not int):
            raise TypeError("The top_floor arg is not of type int.")
        self.top_floor = top_floor
        
        self.moving = False
        self.letting_people_in = False

        if (type(persons_dictionary) is not dict):
            raise TypeError("The persons_dictionary arg is not of type int.")
        self.persons_in_elevator = persons_dictionary

        if (type(buttons_pressed) is not dict):
            raise TypeError("The buttons_pressed arg is not of type int.")
        self.buttons_pressed = buttons_pressed

    def add_passenger(self, passenger):
        """
        Adds a passenger to the elevator. We are assuming it takes 0 seconds to load a passenger.

        Args: 
            passenger: Array where the 0 index is the ID of the passenger, the 1 index is the destination 
            floor of the passenger, and the 2 index is the time that the passenger started waiting at their start floor.

        Returns:
            persons_in_elevator: Dictionary where Keys are a person's ID and Values are a person's.
        """

        person_id = str(passenger[0])
        person_dest_floor = passenger[1]
        person_start_wait_time = passenger[2]
        self.button_pressed(person_dest_floor)
        self.persons_in_elevator[person_id] = [person_dest_floor, person_start_wait_time]
        return self.persons_in_elevator

    def button_pressed(self, button_pressed):
        """
        Updates the buttons that were pressed.

        Args:
            button_pressed: Integer corresponding to the button that was pressed.
            
        Returns:
            buttons_pressed: Dictionary where Keys are the number of floor and Values are the boolean for whether that floor has been pressed or not.
        """

        if button_pressed > self.top_floor or button_pressed < 1:
            raise TypeError("Target floor " + button_pressed + " is not in range of floors.")

        self.buttons_pressed[button_pressed] = True
        return self.button_pressed


    # def wait(self, seconds):
    #     """
    #     Waits for a period of seconds to simulate an action being carried out.
    #     """

    #     self.time = self.time + seconds

    # def open_door(self):
    #     """
    #     Opens the elevator's door.

    #     Returns:
    #         time: Time of the elevator in the simulation.
    #     """
    #     self.busy = False
    #     if not self.door_open:
    #         self.wait(self.wait_time)
    #         self.door_open = True

    #     return self.time

    # def close_door(self):
    #     """
    #     Closes the elevator's door.

    #     Returns:
    #         time: Time of the elevator in the simulation.
    #     """

    #     if self.door_open:
    #         self.wait(self.wait_time)
    #         self.door_open = False

    #     self.busy = True
    #     return self.time

    # def go_to_floor(self, target_floor):
    #     """
    #     Moves the elevator from its current floor to target_floor and unloads everybody.

    #     Args:
    #         target_floor: Float representing the floor that the elevator will go to.

    #     Returns:
    #         elevator_state: Array containing the elevator's time, current location, buttons pressed, and persons that left the elevator at the target floor.
    #     """

    #     if target_floor > self.top_floor or target_floor < 1:
    #         raise TypeError("Target floor " + target_floor + " is not in range of floors.")

    #     original_floor = self.current_floor
    #     time_taken = abs(target_floor - original_floor) * self.wait_time
    #     self.wait(time_taken)
    #     self.current_floor = target_floor
    #     if isinstance(target_floor, int):
    #         self.buttons_pressed[target_floor] = False
    #         persons_that_left = {key:val for key, val in self.persons_in_elevator.items() if val[0] == target_floor}
    #     else:
    #         persons_that_left = {}
    #     elevator_state = [self.time, self.current_floor, self.buttons_pressed, persons_that_left]
    #     return elevator_state