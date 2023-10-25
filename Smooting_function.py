#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:18:26 2023

@author: synnoveronnekleiv
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

file="/Users/synnoveronnekleiv/Downloads/test_1.txt" #Definerer hvilke fil som leses

liste=[] #lager en tom liste (skal inneholde punktene)
x=[] #tom liste, skal inneholde x-verdiene til sigmoidkurva
y=[] #tom liste, skal inneholde y-verdiene til sigmoidkurva

with open (file,'r') as infile: #Åpner fila i lesemodus, fila lukkes automatisk
    lines=infile.readlines() #leser alle linjene og lagrer de
    for line in lines: #Skal gå gjennom alle linjene en for en
        words=line.split() #Splitter på mellomrom, for å skille x og y-verdiene
        if len(words)<2: #Sjekker om words inneholder mindre enn to elementer
            continue #Hvis den inneholder mindre enn to skjer ingen ting
        else: #Hvis ikke går den videre
            liste.append(words) #Appender x og y verdi i en felles liste
            a = words[0].strip(" ") #Fjerner eventuelle mellomrom fra x-verdiene
            b = words[1].strip(" ") #Fjerner eventuelle mellomrom fra y-verdiene
            x.append(float(a)) #Legger x-verdiene i egen liste
            y.append(float(b)) #Legger y verdien i egen liste

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
