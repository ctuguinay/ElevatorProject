import os
import os.path
import numpy as np
import argparse
from numpy import genfromtxt
from matplotlib import pyplot as plt

if __name__ == "__main__":

    # Parser to parse this script's arguments that pertain to our generated data.
    parser = argparse.ArgumentParser(description='Argument parser for viewing the distribution of our dataset.')
    parser.add_argument("--set_width", type=int,
                        help="Sets with of our Maplotlib Canvas.",
                        default=15)
    parser.add_argument("--set_height", type=int,
                        help="Sets height of our Maplotlib Canvas.",
                        default=15)
    args = parser.parse_args()
    width = args.set_width
    height = args.set_height
    
    # Get absolute current path.
    cur_path = os.path.dirname(__file__)

    # Get absolute path to the data.csv file.
    data_path = os.path.relpath('..\\data\\CSVs\\data.csv', cur_path)
    
    # Put data.csv into numpy array.
    data_np = genfromtxt(data_path, delimiter=',')

    # Delete header row.
    data_np = np.delete(data_np, (0), axis=0)

    # Set subplots.
    figure, axis = plt.subplots(2, 2)

    # Set figure width and height.
    figure.set_figwidth(width)
    figure.set_figheight(height)

    # Get numpy array in seconds.
    seconds_np = data_np[:, 1]

    # Convert seconds to hours.
    time_converter = lambda seconds: seconds / 3600
    time_np = np.array([time_converter(seconds.item()) for seconds in seconds_np])

    # Create time entered histogram.
    axis[0,0].hist(time_np)

    # Title time entered histogram.
    axis[0,0].set_title("Time Button Press Histogram (Military Time)")

    # Create start floor histogram.
    axis[0,1].hist(data_np[:, 2])

    # Title start floor histogram.
    axis[0,1].set_title("Start Floor Histogram")

    # Create end floor histogram.
    axis[1,0].hist(data_np[:, 3])

    # Title end floor histogram.
    axis[1,0].set_title("End Floor Histogram")

    # Create person weight histogram.
    axis[1,1].hist(data_np[:, 0])

    # Title person weight histogram plot.
    axis[1,1].set_title("Weight Histogram")

    # Show plot
    plt.show()