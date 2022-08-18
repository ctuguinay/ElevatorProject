import csv
import argparse
import sys
import os

try:
    from data.classes.Person import Person
except:
    from classes.Person import Person

def argparse_create(args):
    """
    Parser to parse this script's arguments that pertain to our generated data.

    Args:
        args: User inputted arguments that have yet to be parsed.

    Returns:
        parsed_args: Parsed user inputted arguments.
    """

    parser = argparse.ArgumentParser(description='Argument parser for creating the genereated dataset CSVs.')

    parser.add_argument("--set_persons", type=int,
                    help="Sets how many people there will be in the generated dataset.",
                    default=1000)

    parser.add_argument("--set_target_file", type=str,
                help="The csv file where data will be sent to. Make sure to include a .csv at the end of the target file's name.",
                default="data.csv")

    parser.add_argument("--set_floors", type=int,
                        help="Sets how many floors there will be in the generated dataset.",
                        default=8)

    parser.add_argument("--set_no_stop_prob", type=float,
                    help="Probability of having no non-standard hall-calls",
                    default=0.7)

    parser.add_argument("--set_max_non_standard_hall_calls", type=int,
                help="Maximum number of non-standard hall calls. If nonzero, number of non-standard hall calls is uniformly chosen from 1 to max",
                default=3)

    parser.add_argument("--set_mean_entry", type=int,
            help="Mean time for entering work (time measured in seconds after midnight).",
            default=32400) # 9am

    parser.add_argument("--set_mean_lunch", type=int,
        help="Mean time for leaving to go to lunch (time measured in seconds after midnight).",
        default=46800) # 1pm

    parser.add_argument("--set_mean_exit", type=int,
        help="Mean time for leaving  work (time measured in seconds after midnight).",
        default=61200) # 5pm

    parser.add_argument("--set_stdev", type=int,
        help="Standard deviation for mean times described.",
        default=1800) # 30mins

    parser.add_argument("--set_cutoff", type=int,
        help="Tail cutoff (for use described in _tail_cutoff_normal_sample in the classes/Person.py file).",
        default=5400) # 90mins

    parser.add_argument("--set_mean_lunch_len", type=int,
        help="Mean lunch length.",
        default=1800) # 30 mins.

    parser.add_argument("--set_lunch_stdev", type=int,
        help="Lunch length standard deviation.",
        default=300) # 5 mins.

    parser.add_argument("--set_lunch_cutoff", type=int,
        help="Lunch cutoff.",
        default=900) # 15 mins.
    
    parser.add_argument("--set_standard_call_buffer", type=int,
        help="Buffer between standard calls and any nonstandard calls.",
        default=900) # 15 mins.

    # Parse arguments.
    parsed_args = parser.parse_args(args)

    return parsed_args
    
if __name__ == "__main__":

    # Get parsed args.
    args = argparse_create((sys.argv[1:]))

    # Set the arguments as variables.
    persons = args.set_persons
    target_file = args.set_target_file
    floors = args.set_floors
    no_stop_prob = args.set_no_stop_prob
    max_non_standard_hall_calls = args.set_max_non_standard_hall_calls
    mean_entry = args.set_mean_entry
    mean_lunch = args.set_mean_lunch
    mean_exit = args.set_mean_exit
    stdev = args.set_stdev
    cutoff = args.set_cutoff
    mean_lunch_len = args.set_mean_lunch_len
    lunch_stdev = args.set_lunch_stdev
    lunch_cutoff = args.set_lunch_cutoff
    standard_call_buffer = args.set_standard_call_buffer

    # Raise value error if target_file does not end with .csv.
    if not target_file.endswith(".csv"):
        raise ValueError("Invalid target file format. Must have a .csv at the end of the file name.")

    # Open the CSV file that we will be writing to.
    with open(os.path.join(sys.path[0],"CSVs",target_file), mode='w+', newline='') as file:

        # Define the CSV writer.
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # Iterate through the given number of people that will enter the building in a day.
        for id in range(persons):

            # Create a new person's elevator route throughout the day.
            person = Person(floors, no_stop_prob, max_non_standard_hall_calls, mean_entry,
                            mean_lunch, mean_exit, stdev, cutoff, mean_lunch_len, lunch_stdev,
                            lunch_cutoff, standard_call_buffer)

            # Set unique person ID.
            person_id = id + 1

            for call in person.calls:

                # Write their information to the CSV
                row = [person_id, call.time, call.start_floor, call.dest_floor, person.weight]
                writer.writerow(row)

    sortedRows = []

    # Open the CSV file that we will be reading.
    with open(os.path.join(sys.path[0],"CSVs", target_file), mode='r', newline='') as file:

        # Define the CSV writer.
        reader = csv.reader(file, delimiter=',', quotechar='"')

        # Sort the rows.
        sortedRows = sorted(reader, key=lambda row: row[1], reverse=False)

    
    # Open the CSV file that we will be writing to.
    with open(os.path.join(sys.path[0],"CSVs", target_file), mode='w', newline='') as file:

        # Define the CSV writer.
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # Write the header row.
        first_row = ["person_id", "time_in_seconds", "start_floor", "dest_floor", "weight"]
        writer.writerow(first_row)

        # Iterate through all the sorted rows.
        for row in sortedRows:
            writer.writerow(row)