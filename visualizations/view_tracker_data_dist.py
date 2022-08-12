import os
import os.path
import numpy as np
import argparse
from numpy import genfromtxt
from matplotlib import pyplot as plt

if __name__ == "__main__":

    # Parser to parse this script's arguments that pertain to our generated data.
    parser = argparse.ArgumentParser(description='Argument parser for viewing the distribution of our dataset.')

    parser.add_argument("--set_target_file", type=str,
                    help="Sets which file in data/CSVs/.... we want to visualize data from.",
                    default="tracker.csv")

    parser.add_argument("--set_width", type=int,
                        help="Sets with of our Maplotlib Canvas.",
                        default=15)

    parser.add_argument("--set_height", type=int,
                        help="Sets height of our Maplotlib Canvas.",
                        default=15)

    # Parse arguments.
    args = parser.parse_args()

    # Set the arguments as variables.
    target_file = args.set_target_file
    width = args.set_width
    height = args.set_height

    # Raise value error if target_file does not end with .csv.
    if not target_file.endswith(".csv"):
        raise ValueError("Invalid target file format. Must have a .csv at the end of the file name.")

    try:
    
        # Get absolute current path.
        cur_path = os.path.dirname(__file__)

        # Get absolute path to the data.csv file.
        data_path = os.path.relpath('..\\simulations\\CSVs\\' + target_file, cur_path)
        
        # Put data.csv into numpy array.
        data_np = genfromtxt(data_path, delimiter=',')

    except:

        raise ValueError("No such target directory exists.")

    # Delete header row.
    data_np = np.delete(data_np, (0), axis=0)

    # Get columns.
    number_samples = data_np[:, 0]
    mean_times = data_np[:, 2]
    median_times = data_np[:, 3]
    max_times = data_np[:, 4]
    sum_times = data_np[:, 5]

    # Set subplots.
    figure, axis = plt.subplots(2, 2)

    # Set figure width and height.
    figure.set_figwidth(width)
    figure.set_figheight(height)

    # Create mean times graph.
    axis[0,0].plot(number_samples, mean_times)

    # Title mean times graph.
    axis[0,0].set_title("Mean Times Plot")
    axis[0,0].set(xlabel='Number of Samples', ylabel='Time in Seconds')

    # Create median times graph.
    axis[0,1].plot(number_samples, mean_times)

    # Title median times graph.
    axis[0,1].set_title("Median Times Plot")
    axis[0,1].set(xlabel='Number of Samples', ylabel='Time in Seconds')

    # Create max times graph.
    axis[1,0].plot(number_samples, max_times)

    # Title max times graph.
    axis[1,0].set_title("Max Times Plot")
    axis[1,0].set(xlabel='Number of Samples', ylabel='Time in Seconds')

    # Create sum times graph.
    axis[1,1].plot(number_samples, sum_times)

    # Title sum times graph.
    axis[1,1].set_title("Sum Times Plot")
    axis[1,1].set(xlabel='Number of Samples', ylabel='Time in Seconds')

    # Hide x labels for top plots.
    for ax in axis.flat:
        ax.label_outer()

    # Show plot
    plt.show()