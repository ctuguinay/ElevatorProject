import os
import csv
import pytest
from simulations.classes.Log import Log, LogPIT
from simulations.classes.TimeList import TimeList, TimeListEvent
from simulations.classes.State import State
from simulations.classes.Elevator import Elevator
from simulations.classes.Model import Model
from simulations.base_case_simulation import argparse_create, load_timelist, initialize_values, state_to_elevator_input

def test_argparse_create():
    """
    Tests is argparse_create has the desired behavior.
    """

    parsed_args = argparse_create(["--python_command", "py"])
    python_command = parsed_args.python_command

    assert python_command == "py"

def test_load_timelist():
    """
    Tests if load_timelist has the desired behavior.
    """

    # Get csv path.
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, "data/CSVs/data_test.csv").replace("simulations\\tests\\", "")

    # Initiliaze Timelist with reader.
    timelist = TimeList()
    with open(full_path, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        timelist = load_timelist(reader,timelist)

    current_event = timelist.next_event()

    assert current_event.time == 31520.846784586633
    assert current_event.object_type == "Hall Call"

    hall_call = current_event.object
    assert hall_call.person_id == 1
    assert hall_call.start_floor == 1
    assert hall_call.dest_floor == 3
    assert hall_call.weight == 93.84930521474159

@pytest.fixture
def preload_timelist():
    """
    Preloads the timelist after we know that load_timelist works as it should.
    """

    # Get csv path.
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, "data/CSVs/data_test.csv").replace("simulations\\tests\\", "")

    # Initialize Timelist with reader.
    timelist = TimeList()
    with open(full_path, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        timelist = load_timelist(reader,timelist)

    return timelist

def test_initialize_values(preload_timelist):
    """
    Test initialize_values for proper behavior.
    """

    timelist = preload_timelist
    assert isinstance(timelist, TimeList)

    _, result_timelist, _, _, _, _ = initialize_values(timelist, -1)

    assert result_timelist == timelist
    assert len(result_timelist.future) == 2

    for event in result_timelist.future:
        assert isinstance(event, TimeListEvent)

    total_time, result_timelist, elevator, current_state, log, model = initialize_values(timelist, 1)

    assert isinstance(total_time, list)
    assert isinstance(result_timelist, TimeList)
    assert isinstance(elevator, Elevator)
    assert isinstance(current_state, State)
    assert isinstance(log, Log)
    assert isinstance(model, Model)

    assert len(result_timelist.future) == 1

    for event in result_timelist.future:
        assert isinstance(event, TimeListEvent)

    log_pit = log.next_log_pit()
    assert isinstance(log_pit, LogPIT)

def test_state_to_elevator_input(preload_timelist):
    """
    Test state_to_elevator_input for proper behavior.
    """

    timelist = preload_timelist
    _, _, _, current_state, _, _ = initialize_values(timelist, -1)

    capacity, curr_weight, curr_pos, buttons_pressed, up_buttons, down_buttons = state_to_elevator_input(current_state)

    assert isinstance(capacity, float)
    assert isinstance(curr_weight, float) or isinstance(curr_weight, int)
    assert isinstance(curr_pos, int) 
    assert isinstance(buttons_pressed, dict)
    assert isinstance(up_buttons, dict)
    assert isinstance(down_buttons, dict)

    for item in buttons_pressed.items():
        assert item[1] == False

    for item in up_buttons.items():
        assert item[1] == False
    
    for item in down_buttons.items():
        assert item[1] == False