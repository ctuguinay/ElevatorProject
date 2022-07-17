from simulations.classes.State import State
from simulations.classes.Elevator import Elevator
import pytest

def test_bad_initialization_state():
    """
    Tests if the State class is working properly with bad initialization.
    """
    
    with pytest.raises(TypeError):
        start_floor = 1
        top_floor = 4
        wait_time = 5
        time = 30000
        elevator_speed = 5
        persons_dictionary = {'1': [4, 30000]}
        buttons_pressed = {1:False, 2: False, 3: False, 4: False}
        elevator = Elevator(start_floor, top_floor, wait_time, time, elevator_speed, persons_dictionary, buttons_pressed)

        up_calls = [1, 2, 3, 4]
        down_calls = {1:False, 2: False, 3: False, 4: False}

        current_intended_destination = 4

        state = State(up_calls, down_calls, current_intended_destination, time, elevator)