import math
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import numpy as np

# =================================================== #
## GET TOTAL TIME IN DATAFRAME

df = pd.read_csv('c:\\Users\\elina\\Desktop\\e436b\\eq1950-2023.csv')
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d')

earliest_eq = min(df['time'])
latest_eq = max(df['time'])
cumu_time = (latest_eq-earliest_eq).days # change to .months or .years as necessary
#print(earliest_eq, latest_eq, cumulative_time) # print for double checking

# =================================================== #
###### IMPORT MAGNITUDES #####

mag_list = df.magnitude.values.tolist() # this list is the entire data base
# print(mag_list) # print for double checking 
mag_list_unique = sorted(df.magnitude.unique().tolist(), reverse=True) # this list is every unique magnitude, from largest -> smallest
# print(mag_list_unique) # print for double checking

# =================================================== #
##### HOW MANY EQ PER MAG #####

events = []

def recur_per(list, list_unique, n_list, i): # i starts at 0
    if i < (len(list_unique)-2):
        count = list.count(list_unique[i])
        n_list.append(count)
        recur_per(list, list_unique, n_list, i+1)
    elif i == (len(list_unique)-1):
        count = list.count(list_unique[i])
        n_list.append(count)
        return n_list
    
# cumulative list
mag_per = recur_per(mag_list, mag_list_unique, events, 0) # how many magnitudes per magnitude?
print(mag_per) # WHY IS IT RETURNING NONE - FIX LATER

# =================================================== #
##### CUMULATE MAGNITUDES #####

l_rank = []

def recur_rank(list, list_unique, n_list, i, j): # i starts at 0, j is the previous total, starts at 0
    if i == 0:
        first = list.count(list_unique[i])
        n_list.append(first)
        recur_rank(list, list_unique, n_list, i+1, first)
    elif i < (len(list_unique)-1):
        new = (list.count(list_unique[i]) + j)
        n_list.append(new)
        recur_rank(list, list_unique, n_list, i+1, new)
    else:
        new = (list.count(list_unique[i]) + j)
        n_list.append(new)
        return n_list

# rank list
ranks = recur_rank(mag_list, mag_list_unique, l_rank, 0, 0) # rank for each magnitude
print(ranks) # WHY IS IT RETURNING NONE - FIX LATER

# =================================================== #
##### CALCULATE FREQUENCY #####

def calc_freq(l_rank, l_tot, l_freq, i):
    if i < len(l_tot):
        freq = l_rank[i]/l_tot[i]
        l_freq.append(freq)
        calc_freq(l_rank, l_tot, l_freq, i+1)
    else:
        return l_freq

# frequency list
frequency = calc_freq(ranks, mag_per, [], 0)
print(frequency)

# =================================================== #
##### MAG/FREQ CHART #####

plt.yscale("log")
plt.scatter(mag_per, frequency)
plt.show()