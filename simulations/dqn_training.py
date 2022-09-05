try:
    from simulations.classes.EventObjects import Arrival, DoorClose, IdleEnd
    from simulations.classes.Elevator import Elevator
    from simulations.classes.State import State
    from simulations.classes.TimeList import TimeList, TimeListEvent
    from simulations.classes.EventObjects import HallCall
    from simulations.classes.Model import Model
    from simulations.classes.Commands import Idle, OpenCloseDoors, Move, Command
    from simulations.classes.Log import Log, LogPIT
    from simulations.classes.DQNAgent import Agent
except:
    from classes.EventObjects import Arrival, DoorClose, IdleEnd
    from classes.Elevator import Elevator
    from classes.State import State
    from classes.TimeList import TimeList, TimeListEvent
    from classes.EventObjects import HallCall
    from classes.Model import Model
    from classes.Commands import Idle, OpenCloseDoors, Move, Command
    from classes.Log import Log, LogPIT
    from classes.DQNAgent import Agent

try:
    from simulations.base_case_simulation import argparse_create, initialize_values, add_to_timelist, state_to_elevator_input
except:
    from base_case_simulation import argparse_create, initialize_values, add_to_timelist, state_to_elevator_input

from numpy import log1p, e
from math import sqrt
from concurrent.futures import process
import os
import sys
import copy
import torch
from typing import Dict, Tuple
import random
import subprocess
import numpy as np
from statistics import mean, median

EPSILON = 0.8 # Set Greedy Strategy constant.

NUM_FLOORS = 8
HEIGHT = {value:key for value in range(1, NUM_FLOORS + 1) for key in [(value - 1) * 4.5]} # A height dict mapping each floor to its height above the ground floor
    # to compute the amount of time it takes to traverse a floor. (Assumes, as is given to us by Google, that
    # the average floor-to-floor height is 4.65 (here glossed as 4.5) m in an office building). Theoretically,
    # this can be altered to create variable distances in the case of a specific building.

SEED = 0 # Sets random seed for the training.

NUMBER_PEOPLE = 1

def initialize_values(timelist, number_samples, return_model):
    """
    Initializes values for the base case simulation.

    Args:
        timelist: Timelist object with all the hall calls.
        number_samples: Integer for max number of samples. If -1, gives all samples.
        return_model: Boolean for whether to return a model.

    Returns:
        total_time: Array that is the initialized total wait time of all people that left the elevator here.
        timelist: Timelist object that has been initialized with a sample of hall calls.
        current_state: State object that has been modified to take into account the most recent event in the simulation.
        elevator: Elevator object that has been properly initialized.
        log: Log object to track every part of the simulation.
        model: Initialized DQN model. Is only returned if return_model is true.
    """

    # Initialize Total Time for all passengers that takes into account wait time and travel time.
    total_time = []

    
    # Sample from full timelist.
    if number_samples != -1:
        full_timelist_future = full_timelist.future
        random.seed()
        future_samples = random.sample(full_timelist_future, number_samples)
        future_samples.sort(key=lambda hall_call: hall_call.time, reverse=False)
        timelist = TimeList()
        timelist.future = future_samples
    else:
        timelist = full_timelist

    # Initialize Elevator.
    floors = list(HEIGHT.keys())
    start_floor = floors[0]
    top_floor = floors[-1]
    capacity = 1500.0
    wait_time = 15
    time = 27000
    elevator_speed = 5
    persons_dictionary = {floor: [] for floor in floors}
    buttons_pressed = {floor: False for floor in floors}
    elevator = Elevator(start_floor, top_floor, capacity, persons_dictionary, buttons_pressed)

    # Initialize current_state.
    up_calls = {floor: [] for floor in floors}
    down_calls = {floor: [] for floor in floors}
    current_state = State(up_calls, down_calls, time, elevator_speed, wait_time, elevator)

    # Initialize Log object and the first LogPIT object and place the LogPIT object into the Log object..
    log = Log()
    start_log_pit = LogPIT(current_state, timelist, [], [])
    log.add_log_pit(start_log_pit)

    # Initialize Model
    if return_model:
        model = Agent(state_size = 26, action_size = 5, seed = SEED)
        return total_time, timelist, elevator, current_state, log, model
    else:
        return total_time, timelist, elevator, current_state, log

def useState(timelist: TimeList, current_state: State, current_event: TimeListEvent, model: Agent, action: Command) -> tuple:
    """
    Makes a single action using the current_state and modifies both the timelist and the current state to match the action.

    Args:
        timelist: TimeList object representing all the events that will occur in the simulation (that we know of).
        current_state: State object representing the current state of the simulation.
        current_event: TimeListEvent object representing the most recent event in the simulation.
        action: Command object representing what the model wishes to do.

    Returns:
        time_list: the timelist, perhaps with events added due to the instructions on what action to take next
        current_state: State object that has been modified to take into account the most recent event in the simulation.
        added_time: the total wait time of all people that left the elevator here.

        reward: If the action given by the model is used, this is the reward given by the
        environment. If not, this is None.
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
    time_diff = current_event.time - current_state.time
    num_people = count_state(current_state)
    curr_reward = - time_diff * num_people
    current_state.aggregated_reward += curr_reward
    reward = current_state.aggregated_reward
    added_time = []

    if current_event == Idle():
        curr_reward *= 10

    if current_state.time > 86400:
        return timelist, current_state, added_time, -10**6, True
    # if num_people > 300:
    #     return timelist, current_state, added_time, -10**4, True

    if not timelist.has_next() and current_event.object_type != "Hall Call" and num_people == 0:
        # there are no hall calls left and nobody's in the elevator. Our work is done, so we return the empty
        # timelist and exit out of the while loop in main
        current_state.aggregated_reward = 0
        return timelist, current_state, added_time, reward, True

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
    
    elif current_event.object_type == "Idle End":

        # nothing happens here

        pass
        

    else:
        raise ValueError("Next event had unexpected type")
    
    if current_state.elevator.moving:
        # the elevator is currently moving between floors so
        # we can't do anything. No need to call the Model, just return with the state we've changed
        
        return timelist, current_state, added_time, None, False


    if current_state.elevator.letting_people_in:
        # TODO: If anyone's on this floor, change state to reflect letting them in to this elevator. We
        # again can't change our behavior, so no need to call the Model, just return with the state we've changed.
        current_state.elevator.moving = False

        # update the passenger
        # person.behavior == "Hall Call"
        # Elevator.persons_in_elevator.add(person)

        if current_state.elevator.going_up:
            #let people who have upcalls into elevator
            current_state.elevator.add_floor(current_state.up_calls)
        else: # going down
            #let people who have downcalls into elevator
            current_state.elevator.add_floor(current_state.down_calls)
        return timelist, current_state, added_time, None, False
    
    # ask the model what to do
    command = action

    #print("------------------------")
    #print(f"buttons_pressed: {buttons_pressed}")
    #print(f"curr_pos: {curr_pos}")
    #print(f"command: {command}")
    #print(current_state.time)

    if type(command) is Idle:

        if not timelist.has_next():
            # add an IdleEnd to stop the timelist from completely emptying out
            new_event = TimeListEvent(current_state.time + 100 # default 100 seconds
            , 'Idle End', IdleEnd())
            timelist.add_event(new_event)
            
        
        current_state.aggregated_reward = 0
        return timelist, current_state, added_time, reward, False

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
            current_state.aggregated_reward = 0
            # treated like an Idle
            if not timelist.has_next():
            # add an IdleEnd to stop the timelist from completely emptying out
                new_event = TimeListEvent(current_state.time + 100 # default 100 seconds
                , 'Idle End', IdleEnd())
                timelist.add_event(new_event)
            return timelist, current_state, added_time, reward, False
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
            current_state.elevator.curr_weight -= person.weight
    

        for person in removed:
            #added_time += current_state.time - person.time
            added_time.append(current_state.time - person.time)
        
        reward += len(removed) * 10000

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

    current_state.aggregated_reward = 0

    return timelist, current_state, added_time, reward, False

def count_state(state: State):
    """Returns the number of people waiting in the state"""
    ct = 0
    for person_list in [state.up_calls, state.down_calls, state.elevator.persons_in_elevator]:
        for floor in person_list:
            for _ in person_list[floor]:
                ct += 1
    return ct
    


def process_state(state, use_tensor = False):
    """
    Processes state so that it can be passed into the model.
    
    Args:
        state: State object that represents the state of the simulation.

    Returns:
        state_array: Numpy or Tensor array that represents the state that can be placed within the model.
    """

    capacity, curr_weight, curr_pos, buttons_pressed, up_buttons, down_buttons = state_to_elevator_input(state)
    total_val = capacity + curr_weight
    temp_array = [capacity/total_val, curr_weight/total_val, curr_pos/NUM_FLOORS]

    for array in [buttons_pressed, up_buttons, down_buttons]:
        for item in array:
            if item:
                temp_array.append(1)
            else:
                temp_array.append(0)
    if use_tensor:
        state_array = torch.tensor(temp_array)
    else:
        state_array = np.array(temp_array)
        
    return state_array

def process_action(action_value):
    """
    Processes action so that it can be passed into the model.
    
    Args:
        action_value: Int that represents the action that can be placed within the model.

    Returns:
        action: Command object that represents the action to take in the simulation.
    """

    if action_value == 0:
        return Idle()
    elif action_value == 1:
        return OpenCloseDoors(True)
    elif action_value == 2:
        return OpenCloseDoors(False)
    elif action_value == 3:
        return Move(True)
    elif action_value == 4: 
        return Move(False)

def process_state_for_input(state:State) -> Tuple[float, float, int,
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
    state_arr = [state.elevator.curr_weight/state.elevator.capacity, \
        curr_pos/NUM_FLOORS]

    for floor, call_list in state.up_calls.items():
        state_arr.append(len(call_list))
    
    for floor, call_list in state.down_calls.items():
        state_arr.append(len(call_list))

    desired_locations = []
    for _ in range(NUM_FLOORS):
        desired_locations.append(0)

    for call_list in state.elevator.persons_in_elevator.values():
        for person in call_list:
            desired_locations[person.dest_floor - 1] += 1
    
    state_arr += desired_locations

    return np.array(state_arr)


if __name__ == "__main__":

    # Get parsed args.
    args = argparse_create((sys.argv[1:]))

    python_command = args.python_command

    gen_script = "data/create_csv.py"

    # Initialize CSV Tracker.
    first_row = ["number_samples", "number_times", "mean_times", "median_times", "max_times", "sum_times"]
    tracker = [first_row]

    # Get csv path.
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, "data", "CSVs", "data.csv").replace("simulations\\", "")

    full_gen_path = script_dir.replace("simulations", "") + gen_script
    subprocess.run([python_command, full_gen_path, f"--set_persons={NUMBER_PEOPLE}", f"--set_floors={NUM_FLOORS}"])

    # Initiliaze Full Timelist with reader.
    full_timelist = TimeList()
    full_timelist = add_to_timelist(full_timelist, full_path)

    for epoch in range(150):

        full_gen_path = script_dir.replace("simulations", "") + gen_script
        subprocess.run([python_command, full_gen_path, f"--set_persons={NUMBER_PEOPLE}", f"--set_floors={NUM_FLOORS}"])

        # Initiliaze Full Timelist with reader.
        full_timelist = TimeList()
        full_timelist = add_to_timelist(full_timelist, full_path)

        # Get initial values.
        if epoch == 0:
            total_time, timelist, elevator, current_state, log, model = initialize_values(full_timelist, -1, True)
        else:
            total_time, timelist, elevator, current_state, log = initialize_values(full_timelist, -1, False)

        #if epoch == 9:
        #    EPSILON = 0

        # Repeat until no more events in timelist.
        count = 0
        done = False
        while not done:
            count += 1
            reward = None
            current_state_copy = copy.deepcopy(current_state)
            while reward is None:
                action = process_action(model.act(process_state_for_input(current_state), EPSILON))
                current_event = timelist.next_event()
                timelist, result_state, added_time, reward, done = useState(timelist, current_state, current_event, model, action)
            loss = model.step(process_state_for_input(current_state_copy),action,reward,process_state_for_input(result_state),done)
            if loss is not None:
                print(np.log(loss))
            weight = 0
            for floor in result_state.elevator.persons_in_elevator:
                for person in result_state.elevator.persons_in_elevator[floor]:
                    weight += person.weight

            total_time = total_time + added_time
            current_log_pit = LogPIT(result_state, timelist, added_time, total_time)
            log.add_log_pit(current_log_pit)
            current_state = result_state

        EPSILON = 0.8

        print(f"Epoch: {epoch + 1}")
        print(f"Number of Events: {count}")

        if len(total_time) > 0:

            # Prints out the length of total_time
            length_total_time = len(total_time)
            #print(length_total_time)

            # Prints out mean of total_time
            mean_total_time = mean(total_time)
            #print(mean_total_time)

            # Prints out median of total_time
            median_total_time = median(total_time)
            #print(median_total_time)

            # Prints out max of total_time
            max_total_time = max(total_time)
            #print(max_total_time)

            # Prints out sum of total_time.
            sum_total_time = length_total_time * mean_total_time
            #print(sum_total_time)

            print(f"Number of People Moved: {length_total_time}")
            print(f"Mean Total Time: {mean_total_time}")
            print(f"Median Total Time: {median_total_time}")
            print(f"Max Total Time: {max_total_time}")
            print(f"Sum Total Time: {sum_total_time}")
        
        else:
            print("Model Has Moved No People.")
