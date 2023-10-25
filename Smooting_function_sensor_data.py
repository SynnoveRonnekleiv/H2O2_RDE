#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:18:26 2023

@author: synnoveronnekleiv
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import csv


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



# Apply the Savitzky-Golay filter
y_smooth = savgol_filter(y, window_length=31, polyorder=3)

# Plot original noisy data and smoothed data
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Noisy data', linestyle='--', alpha=0.7)
plt.plot(x, y_smooth, label='Smoothed data', color='r')
plt.title("Noise Reduction using Savitzky-Golay Filter")
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)
plt.show()
