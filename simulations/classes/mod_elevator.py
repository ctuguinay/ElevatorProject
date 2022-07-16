class Elevator(object):
    """
    Elevator object to help us keep track of elevator parameters and functionalities.

    Args:
        start_floor: Integer for the floor that the elevator starts at.
        top_floor: Integer for the highest floor that the elevator can visit.
        wait_time: Integer for the number of seconds that the elevator waits before it closes the door.
        elevator_speed: Integer for the number of seconds that the elevator takes to go up or down 1 floor.
        persons_dictionary: Dictionary where Keys are a person's ID and Values are a person's 
        time: Integer for the time of the current simulation in seconds.

    Attributes:
        current_floor: Integer for the floor that the elevator is currently at.
        top_floor: Integer for the top floor that the elevator can visit.
        busy: Boolean for if the elevator is busy.
        door_open: Boolean for if the door is open.
        going_up: Boolean for if the elevator is (or was last) going up.
        wait_time: Integer for the number of seconds that the elevator waits before it closes the door.
        elevator_speed: Integer for the number of seconds that the elevator takes to go up or down 1 floor.
        persons_in_elevator: Dictionary where Keys are a person's ID and Values are a person's 
        time: Integer for the time of the current simulation in seconds.
    """

    def __init__(self, start_floor, top_floor, wait_time, time, elevator_speed, persons_dictionary):
        """"
        Initialize elevator object with given parameters.
        """

        self.current_floor = start_floor
        self.top_floor = top_floor
        self.busy = False
        self.door_open = False
        self.going_up = True
        self.wait_time = wait_time
        self.elevator_speed = elevator_speed
        self.persons_in_elevator = persons_dictionary
        self.time = time

    def add_passengers(self, passenger):
        """
        Adds a passenger to the elevator. We are assuming it takes 0 seconds to load a passenger.

        Args: 
            passenger: Array where the first element is the ID of the passenger, and the second element is the destination 
            floor of the passenger.
        """

        person_id = str(passenger[0])
        person_dest_floor = passenger[1]
        self.persons_in_elevator[person_id] = person_dest_floor


    def wait(self, seconds):
        """
        Waits for a period of seconds to simulate an action being carried out.
        """

        self.time = self.time + seconds

    def open_door(self):
        """
        Opens the elevator's door.
        """
        self.busy = False
        if not self.door_open:
            self.wait(2)
            self.door_open = True

    def close_door(self):
        """
        Closes the elevator's door.
        """

        if self.door_open:
            self.wait(2)
            self.door_open = False

        self.busy = True

    def go_to_floor(self, target_floor):
        """
        Moves the elevator from its current floor to target_floor.
        """

        if target_floor not in range(self.top_floor + 1):
            raise ValueError("Target floor " + target_floor + " is not in range of floors.")

        original_floor = self.current_floor
        time_taken = abs(target_floor - original_floor) * self.wait_time
        self.wait(time_taken)