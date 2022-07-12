import os
import os.path
import numpy as np
from numpy import genfromtxt
from matplotlib import pyplot as plt

if __name__ == "__main__":
    
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

    # Set figure height and width.
    figure.set_figheight(15)
    figure.set_figwidth(15)

    # Get numpy array in seconds.
    seconds_np = data_np[:, 1]

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