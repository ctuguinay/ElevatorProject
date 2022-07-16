from hashlib import new
from simulations.classes.Elevator import Elevator
import pytest

def test_elevator():
    """
    Tests if the Elevator class is working properly.
    """
    
    start_floor = 1
    top_floor = 8
    wait_time = 5
    time = 30000
    elevator_speed = 5
    persons_dictionary = {'1':4}
    buttons_pressed = {1:False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, wait_time, time, elevator_speed, persons_dictionary, buttons_pressed)

    new_persons_dictionary = elevator.add_passenger(['3', 4])

    assert new_persons_dictionary['1'] == 4
    assert new_persons_dictionary['3'] == 4

    assert elevator.buttons_pressed == {1:False, 2: False, 3: False, 4: True}

    assert elevator.open_door() == 30005

    elevator_state = elevator.go_to_floor(1.5)

    assert elevator_state[0] == 30007.5
    assert elevator_state[1] == 1.5
    assert elevator_state[2] == {1:False, 2: False, 3: False, 4: True}
    assert elevator_state[3] == {}


    elevator_state = elevator.go_to_floor(4)

    assert elevator_state[0] == 30020
    assert elevator_state[1] == 4
    assert elevator_state[2] == {1:False, 2: False, 3: False, 4: False}
    assert elevator_state[3] == {'1': 4, '3': 4}

    assert elevator.close_door() == 30025



