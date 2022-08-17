from simulations.classes.State import State
from simulations.classes.Elevator import Elevator
import pytest

def test_bad_initialization_state():
    """
    Tests if the State class is working properly with bad initialization.
    """
    
    with pytest.raises(TypeError):

        #Initialize elevator.
        start_floor = 1
        top_floor = 4
        capacity = 1500.0
        persons_dictionary = {}
        buttons_pressed = {1:False, 2: False, 3: False, 4: False}
        elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

        # Initialize current_state.
        up_calls = {1:[], 2:[], 3:[], 4:[]}
        down_calls = []
        time = 27000
        elevator_speed = 5
        wait_time = 15
        state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    with pytest.raises(TypeError):
        
        # Initialize elevator.
        start_floor = 1
        top_floor = 4
        capacity = 1500.0
        persons_dictionary = {}
        buttons_pressed = {1:False, 2: False, 3: False, 4: False}
        elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

        # Initialize current_state.
        up_calls = {1:[], 2:[], 3:[], 4:[]}
        down_calls = {1:[], 2:[], 3:[], 4:[]}
        time = 27000
        elevator_speed = 5
        wait_time = 15.98743983749384739847
        state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    with pytest.raises(TypeError):

        # Initialize an object that is not an elevator.
        not_an_elevator = None

        # Initialize current_state.
        up_calls = {1:[], 2:[], 3:[], 4:[]}
        down_calls = {1:[], 2:[], 3:[], 4:[]}
        time = 27000
        elevator_speed = 5
        wait_time = 15
        state = State(up_calls, down_calls, time, elevator_speed, wait_time, not_an_elevator)

def test_good_intialization():
    """
    Tests if the State class is working properly with good initialization.
    """

    # Initialize an elevator.
    start_floor = 1
    top_floor = 4
    capacity = 1500.0
    persons_dictionary = {}
    buttons_pressed = {1:False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {1:[], 2:[], 3:[], 4:[]}
    down_calls = {1:[], 2:[], 3:[], 4:[]}
    time = 27000
    elevator_speed = 5
    wait_time = 15
    state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)