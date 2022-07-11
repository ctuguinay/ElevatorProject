from turtle import window_height
import numpy as np


class Person:
    """
    Randomly generated information attributed to a single person

    Args:
        floors: number of floors in the building (must be >2)

    Attributes:
        calls: list of Hall_Call objects, representing the hall calls the person made
        weight: the person's weight in kg
    """

    def __init__(self, floors: int):

        # Each person will have a hall call to get to the floor they work on,
        # a hall call to get lunch (on the first floor), a hall call to go back
        # to the floor they work on, and random other hall calls throughout the day

        # -----------------------------------------------------------------------
        # parameters for the data, maybe make some of these into input parameters
        # if ever need be

        # high probability of having no "non-standard" hall-calls
        no_stop_prob = 0.7
        # if nonzero, number of non-standard hall calls is uniformly chosen from 1 to max
        max_non_standard_hall_calls = 3

        # mean time for entering work (time measured in seconds after midnight)
        mean_entry = 32400  # 9am

        # mean lunchtime
        mean_lunch = 46800  # 1pm

        # mean time for exiting work
        mean_exit = 61200  # 5pm

        # standard deviation for "standard times" above
        stdev = 1800  # 20 mins

        # tail cutoff (for use described in _tail_cutoff_normal_sample)
        cutoff = 5400  # 60 mins

        # mean lunch length
        mean_lunch_len = 1800  # 30 mins

        # standard devation for lunch length
        lunch_stdev = 300  # 5 mins

        # tail cutoff for lunch length
        lunch_cutoff = 900  # 15 mins

        # buffer between standard calls and any nonstandard calls
        standard_call_buffer = 900  # 15 mins
        # ------------------------------------------------------------------------

        arrival_time = self._tail_cutoff_normal_sample(mean_entry, stdev, cutoff)
        lunch_time = self._tail_cutoff_normal_sample(mean_lunch, stdev, cutoff)
        lunch_end = lunch_time + self._tail_cutoff_normal_sample(mean_lunch_len, lunch_stdev, lunch_cutoff)
        exit_time = self._tail_cutoff_normal_sample(mean_exit, stdev, cutoff)

        # number of non-standard calls
        if np.random.uniform() < no_stop_prob:
            num_non_standard_calls = 0
        else:
            # if nonzero, uniformly chosen from 1 to max_calls
            num_non_standard_calls = np.random.randint(low=1, high=max_non_standard_hall_calls + 1)
        # equal chance for each non-standard hall call to be pre-lunch or post-lunch
        num_pre_lunch_calls = np.random.binomial(n=num_non_standard_calls, p=0.5)
        num_post_lunch_calls = num_non_standard_calls - num_pre_lunch_calls

        # randomly choose pre_lunch call times uniformly between arrival and lunch, with buffer
        pre_lunch_call_times = []
        for i in range(num_pre_lunch_calls):
            pre_lunch_call_times.append(
                np.random.uniform(arrival_time + standard_call_buffer, lunch_time - standard_call_buffer))
        pre_lunch_call_times.sort()
        # same with post_lunch call times, between lunch_end and exit_time
        post_lunch_call_times = []
        for i in range(num_post_lunch_calls):
            post_lunch_call_times.append(
                np.random.uniform(lunch_end + standard_call_buffer, exit_time - standard_call_buffer))
        post_lunch_call_times.sort()

        self.calls = []

        # randomly choose the floor (excluding the first) that the person works on
        work_floor = np.random.randint(low=2, high=floors + 1)

        # arrival
        arrival_call = Hall_Call(arrival_time, 1, work_floor)
        self.calls.append(arrival_call)

        curr_floor = work_floor
        # non-standard pre-lunch hall calls
        for time in pre_lunch_call_times:
            # disallow the first floor and the current floor for non-standard hall calls
            available_floors = np.concatenate((np.arange(2, curr_floor), np.arange(curr_floor + 1, floors + 1)))
            next_floor = np.random.choice(available_floors)
            self.calls.append(Hall_Call(time, curr_floor, next_floor))
            curr_floor = next_floor

        # leaving for lunch
        lunch_leave_call = Hall_Call(lunch_time, curr_floor, 1)
        self.calls.append(lunch_leave_call)

        # coming back after lunch
        lunch_back_call = Hall_Call(lunch_end, 1, work_floor)
        self.calls.append(lunch_back_call)
        curr_floor = work_floor

        # non-standard post-lunch hall calls (exactly the same)
        for time in post_lunch_call_times:
            available_floors = np.concatenate((np.arange(2, curr_floor), np.arange(curr_floor + 1, floors + 1)))
            next_floor = np.random.choice(available_floors)
            self.calls.append(Hall_Call(time, curr_floor, next_floor))
            curr_floor = next_floor

        # leaving work
        leave_call = Hall_Call(exit_time, curr_floor, 1)
        self.calls.append(leave_call)

        if np.random.binomial(n=1, p=0.5) == 0:
            # male
            self.weight = np.random.normal(loc=91, scale=17)
        else:
            # female
            self.weight = np.random.normal(loc=78, scale=9)

    def _tail_cutoff_normal_sample(self, mean, stdev, cutoff):
        """
        sample from normal distributions but cut off tails at some point
        to prevent unreasonable circumstances (getting to work at 11 pm, etc)
        """
        val = np.random.normal(loc=mean, scale=stdev)
        if val < mean - cutoff:
            return mean - cutoff
        elif val > mean + cutoff:
            return mean + cutoff
        return val


class Hall_Call:
    """
    Information for a single hall call: time,
    start floor, and dest floor
    """

    def __init__(self, time, start_floor, dest_floor):
        self.time = time
        self.start_floor = start_floor
        self.dest_floor = dest_floor

    # just for testing with prints
    def __str__(self):
        return f"(time: {self.time}, start_floor: {self.start_floor}, dest_floor: {self.dest_floor})"

    def __repr__(self):
        return self.__str__()