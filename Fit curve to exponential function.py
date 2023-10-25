#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:33:17 2023

@author: synnoveronnekleiv
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import csv
from matplotlib.widgets import RectangleSelector


infile='/Users/synnoveronnekleiv/Desktop/Peroxygenase experiment/231020 E160N AfAA11B parallell 2.txt' #Definerer hvilke fil som leses

# Initialize lists to store current and corrected time data
y = []
x = []

# Read the input file and extract data
with open(infile, 'r') as file:
    # Skip the first 150 lines
    for _ in range(150):
        next(file)
    
    # Read the remaining lines using CSV reader
    csv_reader = csv.reader(file, delimiter=';')
    for row in csv_reader:
        if len(row) >= 3:
            try:
                current_n = float(row[1])  # Read the value in "n"
                current_nA = current_n * 1000000000  # Convert "n" to "nA"
                time = float(row[2])
                y.append(current_nA)
                x.append(time)
            except ValueError:
                pass  # Skip rows with invalid data

# Convert data lists to numpy arrays
y = np.array(y)
x = np.array(x)

# Funksjon: f(x)=C*e^ax

# Create the original corrected plot
plt.plot(x, y, marker='o', linestyle='-')
plt.xlabel('Corrected Time (s)')
plt.ylabel('Current (nA)')
plt.title('Current vs Corrected Time')
plt.grid(True)  # Add grid lines to the graph
plt.grid(which='minor', linestyle='--', linewidth=0.5)  # Add grid lines for minor ticks
plt.minorticks_on()  # Enable minor ticks
plt.tight_layout()
plt.show()

# Prompt user for a new reduced time scale range for the hydrogen peroxide concentration plot
new_reduced_start_time = float(input("Creating final reduced plot - Enter start time for initial rate of reaction plot: "))
new_reduced_end_time = float(input("Creating final reduced plot - Enter end time for initial rate of reaction plot: "))

# Filter data for the new reduced time scale range
new_reduced_time_range_indices = np.where((x >= new_reduced_start_time) & (x <= new_reduced_end_time))
new_x = x[new_reduced_time_range_indices]-new_reduced_start_time
new_y = y[new_reduced_time_range_indices]

# Create the new reduced plot of hydrogen peroxide concentration versus corrected time
plt.figure()
plt.plot(new_x, new_y, marker='o', linestyle='-')
plt.xlabel('Corrected Time (s)')
plt.ylabel('Hydrogen Peroxide Concentration (uM)')
plt.title('Reduced Hydrogen Peroxide Concentration vs Corrected Time')
plt.grid(True)  # Add grid lines to the graph
plt.grid(which='minor', linestyle='--', linewidth=0.5)  # Add grid lines for minor ticks
plt.minorticks_on()  # Enable minor ticks
plt.xticks(np.arange(new_reduced_start_time, new_reduced_end_time + 1, 5))
plt.tight_layout()
plt.show()


# Apply the Savitzky-Golay filter
y_smooth = savgol_filter(new_y, window_length=31, polyorder=3)

# Plot original noisy data and smoothed data
plt.figure(figsize=(10, 6))
plt.plot(new_x, new_y, label='Noisy data', linestyle='--', alpha=0.7)
plt.plot(new_x, y_smooth, label='Smoothed data', color='r')
plt.title("Noise Reduction using Savitzky-Golay Filter")
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)
plt.show()


# Exponential function: y = a * exp(b * x) + c
def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

# Initial guesses:
a_init = y_smooth[0]
b_init = np.log(y_smooth[-1]/y_smooth[0]) / (new_x[-1] - new_x[0])
c_init = 0

params, covariance = curve_fit(exponential, new_x, y_smooth, p0=[a_init, b_init, c_init])

a_fit, b_fit, c_fit = params


# Plotting
plt.figure(figsize=(10,6))
plt.scatter(new_x, new_y, color='gray', label='Noisy Data', s=10)
#plt.plot(new_x, new_y, 'g-', label='Actual Function')
#plt.plot(new_x, y_smooth, 'r-', label='Smoothed Data')
plt.plot(new_x, exponential(new_x, a_fit, b_fit, c_fit), 'b--', label=f'Fitted Function: {a_fit:.2f} * exp({b_fit:.2f} * x)')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fitting Smoothed Data to an Exponential Function')
plt.grid(True)
plt.show()


print(f'Fitted Function: {a_fit:.2f} * exp({b_fit:.2f} * x)')