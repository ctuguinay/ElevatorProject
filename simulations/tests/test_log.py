from multiprocessing.sharedctypes import Value
import pytest
from simulations.classes.Log import Log, LogPIT
from simulations.classes.TimeList import TimeList, TimeListEvent
from simulations.classes.State import State
from simulations.classes.Elevator import Elevator


def test_general_LogPIT_initialization():
    """
    Tests general initializations for the LogPIT class with realistic values.
    """

    # Initilize Timelist.
    timelist = TimeList()
  
    # Initialize Timelist event.
    time = 27005
    object_type = "Button Press"
    person_info = [859,27005,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
    timelist_event = TimeListEvent(time, object_type, person_info)

    # Add to Timelist.
    timelist.add_event(timelist_event)

    # Initialize an elevator.
    start_floor = 1
    top_floor = 4
    persons_dictionary = {}
    buttons_pressed = {1:False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {1:[], 2:[], 3:[], 4:[]}
    down_calls = {1:[], 2:[], 3:[], 4:[]}
    time = 27000
    elevator_speed = 5
    wait_time = 15
    state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    # Initialize added and total time.
    added_time = []
    total_time = []

    log_pit = LogPIT(state, timelist, added_time, total_time)

    # Check if initialization works.
    assert log_pit.result_state == state
    assert log_pit.timelist == timelist
    assert log_pit.added_time == added_time
    assert log_pit.total_time == total_time

def test_bad_LogPIT_initialization():
    """
    Tests bad initializations for the LogPIT class with semi-realistic values.
    """

    # Initilize Timelist.
    timelist = TimeList()
  
    # Initialize Timelist event.
    time = 27005
    object_type = "Button Press"
    person_info = [859,27005,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
    timelist_event = TimeListEvent(time, object_type, person_info)

    # Add to Timelist.
    timelist.add_event(timelist_event)

    # Initialize an elevator.
    start_floor = 1
    top_floor = 4
    persons_dictionary = {}
    buttons_pressed = {1:False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {1:[], 2:[], 3:[], 4:[]}
    down_calls = {1:[], 2:[], 3:[], 4:[]}
    time = 27000
    elevator_speed = 5
    wait_time = 15
    state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    # Initialize added and total time.
    added_time = []
    total_time = []


    with pytest.raises(TypeError):
        log_pit = LogPIT(state)

    with pytest.raises(TypeError):
        log_pit = LogPIT(state, state, added_time)
    
    with pytest.raises(TypeError):
        log_pit = LogPIT(state, timelist, added_time)
    
    with pytest.raises(TypeError):
        log_pit = LogPIT(state, added_time, total_time)

def test_general_Log_behavior():
    """
    Tests general initializations for the Log class with realistic values.
    """

    # Initilize Timelist.
    timelist = TimeList()
  
    # Initialize Timelist event.
    time = 27005
    object_type = "Button Press"
    person_info = [859,27005,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
    timelist_event = TimeListEvent(time, object_type, person_info)

    # Add to Timelist.
    timelist.add_event(timelist_event)

    # Initialize an elevator.
    start_floor = 1
    top_floor = 4
    persons_dictionary = {}
    buttons_pressed = {1:False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {1:[], 2:[], 3:[], 4:[]}
    down_calls = {1:[], 2:[], 3:[], 4:[]}
    time = 27000
    elevator_speed = 5
    wait_time = 15
    state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    # Initialize added and total time.
    added_time = []
    total_time = []

    # Initialize Log PIT object.
    log_pit = LogPIT(state, timelist, added_time, total_time)

    # Initialize Log object.
    log = Log()

    # Check if add_log_pit and next_log_pit works.
    
    log.add_log_pit(log_pit)
    first_next = log.next_log_pit()
    first_pointer = log.return_pointer()
    second_next = log.next_log_pit()
    second_pointer = log.return_pointer()

    assert first_next == log_pit
    assert first_pointer == 1
    assert second_next == None
    assert second_pointer == 1

    with pytest.raises(TypeError):
        empty_array = []
        log.add_log_pit(empty_array)

    # Check if length works.

    assert log.length() == 1

    # Check if pointer works.

    assert log.return_pointer() == 1

    # Check if change_pointer works.

    log.change_pointer(0)
    
    assert log.return_pointer() == 0

    log.change_pointer(1)

    assert log.return_pointer() == 1

    with pytest.raises(ValueError):
        log.change_pointer(2)