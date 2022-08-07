from classes.EventObjects import Arrival, DoorClose
from classes.Elevator import Elevator
from classes.State import State
from classes.TimeList import TimeList, TimeListEvent
from classes.EventObjects import HallCall
from classes.Model import Model
from classes.Commands import Idle, OpenCloseDoors, Move
from classes.Log import Log, LogPIT


from math import log1p, e
import csv
import os
from typing import Tuple, Dict


HEIGHT = {1: 0, 2: 4.5, 3: 9, 4: 13.5} # A height dict mapping each floor to its height above the ground floor
    # to compute the amount of time it takes to traverse a floor. (Assumes, as is given to us by Google, that
    # the average floor-to-floor height is 4.65 (here glossed as 4.5) m in an office building). Theoretically,
    # this can be altered to create variable distances in the case of a specific building.


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

    for row in reader:
        if row[0] == "person_id":
            continue
        row_obj = HallCall(
            int(row[0]), # person_id
            float(row[1]), # time of the call
            int(row[2]), # start_floor
            int(row[3]), # dest floor
            float(row[4]) # weight
        )
        timelist.add_event(TimeListEvent(
            float(row[1]), # time
            "Hall Call", # these are all hall calls
            row_obj
        ))

    return timelist

def useState(timelist: TimeList, current_state: State, current_event: TimeListEvent, model: Model) -> tuple:
    """
    Makes a single action using the current_state and modifies both the timelist and the current state to match the action.

    Args:
        item: TimeListEvent object representing the most recent event in the simulation.
        current_state: State object representing the current state of the simulation.

    Returns:
        time_list: the timelist, perhaps with events added due to the instructions on what action to take next
        current_state: State object that has been modified to take into account the most recent event in the simulation.
        added_time: the total wait time of all people that left the elevator here
    """

    """
    TODO:
        I'll give an explanation of the classes at play in general, then explain some steps for implementing 
        this method. For more details on the classes' constructors, attributes, and methods, feel free to 
        read the extensive documentation above each class (enormous thanks to Ceasar!). 
        
        The main data structure in use here is the "timelist", a timeline 
        of events that will occur in the future. For every iteration of the while loop in main, we take the next
        TimeListEvent off the list and use it to determine what to do next (which occurs in this method). Each
        TimeListEvent consists of a time (the time when the event happens), a string describing what is happening,
        and an object (one of the objects listed in EventObjects) with some extra information.

        A State object describes the State of the entire system. For example, the time attribute of State
        is the current time in the system. The State object contains an Elevator object, which describes the
        state of the Elevator.

        A Model is an ML Model or algorithm that tells us what to do given a certain state. It gives instructions
        in the form of Commands. There are three possible Commands: Idle (do nothing), OpenCloseDoors (representing
        the entire process of opening and closing the doors to let people in and out), and Move (go up a floor)
        or down a floor. The current Model is a dummy Model that just tells us to Idle any time we ask it
        for an instruction--we won't make it more sophisticated for now, because making a more sophisticated
        model will probably be the job of the team working on ML for the rest of the project.

        The purpose of this method is to take in the timelist, current state, and next event for consideration, 
        ask the model what to do, and update the timelist and current state accordingly.
    """

    # We update the total time waited (which is the sum of (<time arrived at dest> - <time when started waiting>) 
    # across all hall calls) whenever people get to their destination. added_time will be the amount by 
    # which we increment the total time waited by as a result of people getting to their destination during this event,
    # which will sometimes happen on Arrival events
    added_time = 0

    if not timelist.has_next() and current_event.object_type != "Hall Call" and current_state.elevator.total_passenger_weight() == 0:
        # there are no hall calls left and nobody's in the elevator. Our work is done, so we return the empty
        # timelist and exit out of the while loop in main
        return timelist, current_state, added_time

    # TODO: The first thing we do is modify the attributes that can be modified without knowing the model's
    # output (which is the command telling us the next thing to do).
    # For example, we advance the state's time to the time of this event
    current_state.time = current_event.time

    
    if current_event.object_type == "Arrival":
        # TODO: Things that are specific to arrivals, like setting current_state.elevator.moving to false and
        current_state.elevator.moving = False
        current_state.elevator.current_floor = current_event.object.floor
    
    elif current_event.object_type == "Hall Call":
        # TODO: Things that are specific to Hall Calls, like adding the people the up_calls or down_calls lists
        if current_event.object.dest_floor > current_state.elevator.current_floor:
            current_state.up_calls[current_event.object.start_floor].append(current_event.object)
        else: # destination < current_event.start_floor
            current_state.down_calls[current_event.object.start_floor].append(current_event.object)

    elif current_event.object_type == "Door Close":
        # TODO: Things that are specific to Door Close, like setting current_state.elevator.letting_people_in to False
        current_state.elevator.letting_people_in = False
        current_state.elevator.going_up = None
        
    

    else:
        raise ValueError("Next event had unexpected type")
    
    if current_state.elevator.moving:
        # the elevator is currently moving between floors so
        # we can't do anything. No need to call the Model, just return with the state we've changed
        return timelist, current_state, added_time


    if current_state.elevator.letting_people_in:
        # TODO: If anyone's on this floor, change state to reflect letting them in to this elevator. We
        # again can't change our behavior, so no need to call the Model, just return with the state we've changed.
        current_state.elevator.moving = False

        # update the passenger
        # person.behavior == "Hall Call"
        # Elevator.persons_in_elevator.add(person)

        if current_state.elevator.going_up:
            #let people who have upcalls into elevator
            current_state.elevator.add_floor(up_calls)
        else: # going down
            current_state.elevator.add_floor(down_calls)

        return timelist, current_state, added_time
    
    # ask the model what to do
    curr_pos, buttons_pressed, up_buttons, down_buttons = state_to_elevator_input(current_state)
    command = model.get_command(curr_pos, buttons_pressed, up_buttons, down_buttons)

    #print("------------------------")
    #print(f"buttons_pressed: {buttons_pressed}")
    #print(f"curr_pos: {curr_pos}")
    #print(f"command: {command}")
    #print(current_state.time)

    if type(command) is Idle:
        return timelist, current_state, added_time

    elif type(command) is Move:
        
        def journey_time() -> int:
            start = current_state.elevator.current_floor
            end = start + 1 # not sure what to do here... will speak to Mark -Raymond

            # one possible approach below using sigmoid functions to model the accelerating and
            # deccelerating periods, solved for the distance traversed
            PERCENT_ACCELERATING = 0.2 # Represents the percentage of time it takes to accelerate to
                # top speed when going from one floor to the one immediately above.

            def variable_if_arrival():
                """ 
                Gives the time taken to traverse the floors if the elevator is stopping at the
                next floor.
                """
                floors = abs(start - end)
                return ((((current_state.elevator_speed ** -1) / 4) ** -1) * floors + 
                        5 * PERCENT_ACCELERATING - 0.5 * PERCENT_ACCELERATING * (log1p(e ** 5) - 5)) // 5

            def variable_if_continuing():
                """
                Gives the time taken to traverse the floors if the elevator is not stopping at
                the next floor.
                """
                floors = abs(start - end)
                return ((((current_state.elevator_speed ** -1) / 4) ** -1) * floors + 
                        0.5 * PERCENT_ACCELERATING * (log1p(e ** 5) + 5)) // 5 + PERCENT_ACCELERATING

            # temporarily
            return current_state.elevator_speed

        arrival_floor = None
        if command.if_up == True:
            arrival_floor = current_state.elevator.current_floor + 1
        else:
            arrival_floor = current_state.elevator.current_floor - 1
        if arrival_floor < 1 or arrival_floor > current_state.elevator.top_floor:
            # If the model gives us invalid instructions, just idle
            return timelist, current_state, added_time
        arrival_time = current_state.time + journey_time()
        new_event = TimeListEvent(arrival_time, 'Arrival', Arrival(arrival_floor))
        timelist.add_event(new_event)

    elif type(command) is OpenCloseDoors:

        removed = []
        for floor_list in current_state.elevator.persons_in_elevator.values():
            for person in floor_list:
                if person.dest_floor == current_state.elevator.current_floor:
                    removed.append(person)
        
        for person in removed:
            current_state.elevator.persons_in_elevator[person.start_floor].remove(person)
    

        for person in removed:
            added_time += current_state.time - person.time

        if command.going_up:
            calls = current_state.up_calls
        else:
            calls = current_state.down_calls

        current_state.elevator.going_up = command.going_up
        current_state.elevator.add_floor(calls)
        current_state.elevator.letting_people_in = True
        current_state.elevator.buttons_pressed[current_state.elevator.current_floor] = False

        new_event = TimeListEvent(current_state.time + current_state.wait_time, 'Door Close', DoorClose())

        timelist.add_event(new_event)

    else:
        raise ValueError("Return from Model had unexpected type")

    return timelist, current_state, added_time

def state_to_elevator_input(state:State) -> Tuple[int,
        Dict[int,bool],Dict[int,bool],Dict[int,bool]]:
    """
    Arguments:
        state: the state to be transformed
    Takes a state and process it into the information the model is supposed to have
    when it gets called. Specifically, this returns, in order: the elevator's current
    position, the buttons pressed within the elevator (dict from floor num to if made), 
    the up_calls that have been made (dict from floor num to if made), 
    and the down_calls that have been made (dict from floor num to if made)
    """
    curr_pos = state.elevator.current_floor
    buttons_pressed = state.elevator.buttons_pressed
    up_buttons = {}
    for floor, call_list in state.up_calls.items():
        if call_list == []:
            up_buttons[floor] = False
        else:
            up_buttons[floor] = True
    
    down_buttons = {}
    for floor, call_list in state.down_calls.items():
        if call_list == []:
            down_buttons[floor] = False
        else:
            down_buttons[floor] = True
    return curr_pos, buttons_pressed, up_buttons, down_buttons

# def getTotalEventTimes(result_state):
#     """
#     Gets the total wait and travel times of passengers that have finished their travelling in THIS particular event.

#     Args:
#         result_state: State object representing the 
#         current_state: State object representing the current state of the simulation.

#     Returns:
#         total_event_times: Integer for the total wait and travel time in seconds of passengers that have finished their 
#         travelling in THIS particular event
#     """

#     total_event_times = 0

#     """
#     WHAT NEEDS TO BE DONE: Logic for adding onto total_event_times using what is given to us in result state.
#     """

#     return total_event_times

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
    floors = list(HEIGHT.keys())
    start_floor = floors[0]
    top_floor = floors[-1]
    wait_time = 15
    time = 27000
    elevator_speed = 5
    persons_dictionary = {floor: [] for floor in floors}
    buttons_pressed = {floor: False for floor in floors}
    elevator = Elevator(start_floor, top_floor, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {floor: [] for floor in floors}
    down_calls = {floor: [] for floor in floors}
    current_state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    # Initialize Log object and the first LogPIT object and place the LogPIT object into the Log object..
    log = Log()
    start_log_pit = LogPIT(current_state, timelist, [], [])
    log.add_log_pit(start_log_pit)

    # Repeat until no more events in timelist.
    model = Model()
    while timelist.has_next():
        current_event = timelist.next_event()
        timelist, result_state, added_time = useState(timelist, current_state, current_event, model)
        total_time = total_time + added_time
        # Uncomment these after Jeffrey's work gets merged.
        # current_log_pit = LogPIT(result_state, timelist, added_time, total_time)
        # log.add_log_pit(current_log_pit)
        current_state = result_state

    # Prints out the total time.
    print(total_time)