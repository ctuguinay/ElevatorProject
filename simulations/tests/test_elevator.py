from simulations.classes.Elevator import Elevator
import pytest

def test_bad_initialization_elevator():
    """
    Tests if the State class is working properly with bad initialization.
    """
    
    with pytest.raises(TypeError):
        start_floor = 1.3434545
        top_floor = 4
        elevator_speed = 5
        capacity = 1500.0
        persons_dictionary = {}
        buttons_pressed = {1: False, 2: False, 3: False, 4: False}
        elevator = Elevator(start_floor, top_floor, capacity, elevator_speed, persons_dictionary, buttons_pressed)

    with pytest.raises(TypeError):
        start_floor = 1
        top_floor = 4
        elevator_speed = 5
        capacity = 1500.0
        persons_dictionary = {}
        buttons_pressed = {1: False, 2: False, 3: False, 4: False}
        elevator = Elevator(start_floor, top_floor, capacity, elevator_speed, persons_dictionary, buttons_pressed)

    with pytest.raises(TypeError):
        start_floor = 1.343435345
        top_floor = 4
        persons_dictionary = 1
        capacity=1500.0
        buttons_pressed = {1: False, 2: False, 3: False, 4: False}
        elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

def test_good_initialization_elevator():
    """
    Tests if the Elevator class is working properly with good intialization.
    """

    start_floor = 1
    top_floor = 4
    persons_dictionary = {}
    capacity=1500.0
    buttons_pressed = {1: False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

    assert elevator.current_floor == 1
    assert elevator.top_floor == 4
    assert elevator.moving == False
    assert elevator.letting_people_in == False
    assert elevator.persons_in_elevator == {}
    assert elevator.buttons_pressed == {1:False, 2: False, 3: False, 4: False}

@pytest.fixture
def create_empty_elevator():
    """
    Creates an empty elevator.

    Returns:
        empty_elevator: An elevator object which is empty and has been properly initialized.
    """

    start_floor = 1
    top_floor = 4
    persons_dictionary = {}
    buttons_pressed = {1: False, 2: False, 3: False, 4: False}
    capacity = 1500.0
    empty_elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

    return empty_elevator

# def test_add_passenger(create_empty_elevator):
#     """
#     Tests whether the function for adding a passenger works.
#     """

#     empty_elevator = create_empty_elevator

#     new_persons_dictionary = empty_elevator.add_passenger(['3', 4, 30000])

#     assert new_persons_dictionary['3'] == [4, 30000]

#     assert empty_elevator.buttons_pressed == {1:False, 2: False, 3: False, 4: True}