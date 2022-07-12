from classes.Person import Person
import csv
import argparse
import operator

if __name__ == "__main__":

    # Parser to parse this script's arguments that pertain to our generated data.
    parser = argparse.ArgumentParser(description='Argument parser for creating the genereated dataset CSVs.')
    parser.add_argument("--set_floors", type=int,
                        help="Sets how many floors there will be in the generated dataset.",
                        default=8)
    parser.add_argument("--set_persons", type=int,
                        help="Sets how many people there will be in the generated dataset.",
                        default=10000)
    args = parser.parse_args()
    floors = args.set_floors
    persons = args.set_persons

    # Open the CSV file that we will be writing to.
    with open("CSVs/data.csv", mode='w', newline='') as file:

        # Define the CSV writer.
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # Iterate through the given number of people that will enter the building in a day.
        for id in range(persons):

            # Create a new person's elevator route throughout the day.
            person = Person(floors)

            # Set unique person ID.
            person_id = id + 1

            for call in person.calls:

                # Write their information to the CSV
                row = [person_id, call.time, call.start_floor, call.dest_floor, person.weight]
                writer.writerow(row)

    sortedRows = []

    # Open the CSV file that we will be reading.
    with open("CSVs/data.csv", mode='r', newline='') as file:

        # Define the CSV writer.
        reader = csv.reader(file, delimiter=',', quotechar='"')

        # Sort the rows.
        sortedRows = sorted(reader, key=lambda row: row[1], reverse=False)

    
    # Open the CSV file that we will be writing to.
    with open("CSVs/data.csv", mode='w', newline='') as file:

        # Define the CSV writer.
        writer = csv.writer(file, delimiter=',', quotechar='"')

        # Write the header row.
        first_row = ["person_id", "time_in_seconds", "start_floor", "dest_floor", "weight"]
        writer.writerow(first_row)

        # Iterate through all the sorted rows.
        for row in sortedRows:
            writer.writerow(row)