from classes.Elevator import Elevator
from classes.State import State
from classes.TimeList import TimeList, TimeListEvent
import csv
import os

def loadTimeList(reader, timelist):
    """
    Loads the timelist object with timelist events that are made from the rows in reader.

    Args:
        reader: Reader object that has read our input csv.
        timelist: Newly initialized TimeList object.

    Returns:
        timelist: TimeList object filled with TimeListEvents containing information from the reader.
    """

    """
    WHAT NEEDS TO BE DONE: Use reader somewhere here to load the timelist object.
    """

    return timelist

def useState(timelist, current_state, current_event):
    """
    Makes a single action using the current_state and modifies both the timelist and the current state to match the action.

    Args:
        item: TimeListEvent object representing the most recent event in the simulation.
        current_state: State object representing the current state of the simulation.

    Returns:
        current_state: State object that has been modified to take into account the most recent event in the simulation.
    """

    """
    WHAT NEEDS TO BE DONE: Logic for selecting action and modify timelist and current_state in correspondance with said action.
    """

    return timelist, current_state

def getTotalEventTimes(result_state):
    """
    Gets the total wait and travel times of passengers that have finished their travelling in THIS particular event.

    Args:
        result_state: State object representing the 
        current_state: State object representing the current state of the simulation.

    Returns:
        total_event_times: Integer for the total wait and travel time in seconds of passengers that have finished their 
        travelling in THIS particular event
    """

    total_event_times = 0

    """
    WHAT NEEDS TO BE DONE: Logic for adding onto total_event_times using what is given to us in result state.
    """

    return total_event_times

if __name__ == "__main__":

    # Initialize Total Time for all passengers that takes into account wait time and travel time.
    total_time = 0

    # Get csv path.
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, "data/CSVs/data_example.csv").replace("simulations\\", "")

    # Initiliaze Timelist with reader.
    timelist = TimeList()
    with open(full_path, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        timelist= loadTimeList(reader,timelist)

    # Initialize Elevator.
    start_floor = 1
    top_floor = 4
    wait_time = 15
    time = 27000
    elevator_speed = 5
    persons_dictionary = {}
    buttons_pressed = {1:False, 2: False, 3: False, 4: False}
    elevator = Elevator(start_floor, top_floor, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {1:[], 2:[], 3:[], 4:[]}
    down_calls = {1:[], 2:[], 3:[], 4:[]}
    current_intended_destination = None
    current_state = State(up_calls, down_calls, current_intended_destination, time, elevator_speed, wait_time, elevator)

    # Repeat until no more events in timelist.
    while timelist.has_next():
        current_event = timelist.next_event()
        timelist, result_state = useState(timelist, current_state, current_event)
        total_time = getTotalEventTimes(result_state) + total_time
        current_state = result_state

    # Prints out the total time.
    print(total_time)