from classes.Elevator import Elevator
from classes.State import State
from classes.TimeList import TimeList, TimeListEvent
from classes.EventObjects import HallCall
from classes.Model import Model
from classes.Commands import Idle, OpenCloseDoors, Move
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

def useState(timelist, current_state, current_event, model):
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

    if not timelist.has_next() and current_event.object_type != "Hall Call" and len(current_state.elevator.persons_in_elevator) == 0:
        # there are no hall calls left and nobody's in the elevator. Our work is done, so we return the empty
        # timelist and exit out of the while loop in main
        return timelist, current_state, added_time

    # TODO: The first thing we do is modify the attributes that can be modified without knowing the model's
    # output (which is the command telling us the next thing to do).
    # For example, we advance the state's time to the time of this event
    current_state.time = current_event.time
    
    if current_event.object_type == "Arrival":
        # TODO: Things that are specific to arrivals, like setting current_state.elevator.moving to false and
        # computing added_time
        pass
    elif current_event.object_type == "Hall Call":
        # TODO: Things that are specific to Hall Calls, like adding the people the up_calls or down_calls lists
        pass
    elif current_event.object_type == "Door Close":
        # TODO: Things that are specific to Door Close, like setting current_state.elevator.letting_people_in to False
        pass
    else:
        raise ValueError("Next event had unexpected type")
    
    if current_state.elevator.moving:
        # the elevator is currently moving between floors so
        # we can't do anything. No need to call the Model, just return with the state we've changed
        return timelist, current_state, added_time


    if current_state.elevator.letting_people_in:
        # TODO: If anyone's on this floor, change state to reflect letting them in to this elevator. We
        # again can't change our behavior, so no need to call the Model, just return with the state we've changed.
        return timelist, current_state, added_time
    
    # ask the model what to do
    command = model.get_command(current_state)
    if type(command) is Idle:
        # TODO Make any changes that must be made in the context of an Idle command (this might be no changes)
        pass
    elif type(command) is Move:
        # TODO Make any changes that must be made in the context of a Move command, including
        # adding an Arrival event to the timelist, indicating the event of us arriving at the floor. Also
        # make checks to ensure we're not going a floor down from the ground floor or a floor up from the top
        # floor (throw an error if we are)
        pass
    elif type(command) is OpenCloseDoors:
        # TODO Make any changes that must be made in the context of an OpenCloseDoors command, including
        # adding a DoorClose to the timelist, indicating the ending of the process of "letting people in"
        pass
    else:
        raise ValueError("Return from Model had unexpected type")

    # set the new intended destination accordingly
    current_state.current_intended_destination = command.intended_destination

    return timelist, current_state, added_time

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
    model = Model()
    while timelist.has_next():
        current_event = timelist.next_event()
        timelist, result_state, added_time = useState(timelist, current_state, current_event, model)
        # total_time = getTotalEventTimes(result_state) + total_time
        current_state = result_state

    # Prints out the total time.
    print(total_time)