import os
import csv
import pytest
from simulations.classes.Log import Log, LogPIT
from simulations.classes.TimeList import TimeList, TimeListEvent
from simulations.classes.State import State
from simulations.classes.Elevator import Elevator
from simulations.base_case_simulation import load_timelist, initialize_values, state_to_elevator_input

def test_load_timelist():
    """
    Tests if load_timelist works.
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

# TODO: def test_initialize_values():
    """
    Test initialize_values for proper behavior.
    """

# TODO: def test_state_to_elevator_input():
    """
    Test state_to_elevator_input for proper behavior.
    """