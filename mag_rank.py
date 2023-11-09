from datetime import datetime
from dateutil.relativedelta import relativedelta as rd
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import seaborn as sns

# =================================================== #
##### IMPORT CSV #####
# csv must have at minimum a magnitude and time column
# use \\ instead of \ in filepath name

df = pd.read_csv('C:\\Users\\elina\\Desktop\\e436b\\eq1950-2023.csv') 

# =================================================== #
##### GET TOTAL TIME IN DATAFRAME #####
# time column header may vary by file, change as necessary

df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d')
earliest_eq = min(df['time']) 
latest_eq = max(df['time'])

# for total time in years
time_yr = rd(latest_eq, earliest_eq).years
# for total time in months
time_mo = rd(latest_eq, earliest_eq).months + (time_yr*12)
# for total time in days
time_day = (latest_eq-earliest_eq).days

# =================================================== #
###### IMPORT MAGNITUDES #####
# magnitude column header may vary by file, change as necessary

mag_list = df.magnitude.values.tolist() # this list is the entire data base
mag_list_unique = sorted(df.magnitude.unique().tolist(), reverse=True) # this list is every unique magnitude, from largest -> smallest

# =================================================== #
##### HOW MANY EVEMTS PER MAG #####

L_events = []

def LoE(list, list_unique, n_list, i):
    '''
    Outputs n_list with how many events per unique magnitude (found in list_unique) in list.
    recur_per: List List List Int -> List
    Requires: i = 0
    '''
    if i < (len(list_unique)):
        count = list.count(list_unique[i])
        n_list.append(count)
        LoE(list, list_unique, n_list, i+1)
    return n_list
    
# events per magnitude list
events = LoE(mag_list, mag_list_unique, L_events, 0)

# =================================================== #
##### RANK FOR EACH MAGNITUDE #####

l_rank = []

def LoR(list, list_unique, n_list, i, j):
    '''
    Outputs n_list with rank for each unique magnitude (found in list_unique) in list.
    recur_rank: List List List Int Int -> List
    Requires: i = 0, j = 0
    '''
    if i == 0:
        first = list.count(list_unique[i])
        n_list.append(first)
        LoR(list, list_unique, n_list, i+1, first)
    elif i < (len(list_unique)):
        new = (list.count(list_unique[i]) + j)
        n_list.append(new)
        LoR(list, list_unique, n_list, i+1, new)
    return n_list

# rank list
ranks = LoR(mag_list, mag_list_unique, l_rank, 0, 0)

# =================================================== #
##### CALCULATE FREQUENCY FOR EACH MAGNITUDE #####

def calc_freq(l_rank, time, l_freq, i):
    '''
    Outputs l_freq with frequency for each unique magnitude. 
    Item order will be the same as mag_list_unique.
    calc_freq: List List List Int -> List
    Requires: i = 0
    '''
    if i < (len(l_rank)):
        freq = l_rank[i]/time
        l_freq.append(freq)
        calc_freq(l_rank, time, l_freq, i+1)
    return l_freq

# frequency list
frequency_day = calc_freq(ranks, time_day, [], 0)
frequency_mo = calc_freq(ranks, time_mo, [], 0)
frequency_yr = calc_freq(ranks, time_yr, [], 0)

# export magnitude/frequencies as csv
# strongly suggest commenting out code after first export to prevent repetitive exports
#'''
dict = {'magnitude': mag_list_unique, 'frequency (yr)': frequency_yr, 'frequency (mo)': frequency_mo, 'frequency (day)': frequency_day}     
exp = pd.DataFrame(dict)
exp.to_csv('C:\\Users\\elina\\Desktop\\e436b\\magfreq.csv')
#'''

# =================================================== #
##### MAG/FREQ CHART DISPLAY #####

# axis for easier reference
x = mag_list_unique
y_day = frequency_day
y_mo = frequency_mo
y_yr = frequency_yr

# chart settings
plt.rc('axes', axisbelow=True) # display 
plt.yscale("log") # log scale
plt.title('Magnitude/Frequency Occurrence of Major Earthquakes in the CSZ Since 1923')
plt.xlabel("Magnitude") # x-axis label
plt.ylabel("Frequency") # y-axis label
plt.grid(which = 'major', axis = 'y', linewidth = 0.75) # major axis display
plt.grid(which = 'minor', axis = 'y', linewidth = 0.5) # minor axis display
plt.xlim(4.5, 10) # x-axis range

# scatter plot by unit of time, hide as necessary
plot_day = plt.scatter(x, y_day)
plot_mo = plt.scatter(x, y_mo)
plot_yr = plt.scatter(x, y_yr)

# fit trendlines - power, hide as necessary
popt_d, pcov_d = curve_fit(lambda fx,a,b: a*fx**-b, x, y_day)
power_day = popt_d[0]*x**-popt_d[1]
#print(power_day)

popt_m, pcov_m = curve_fit(lambda fx,a,b: a*fx**-b, x, y_mo)
power_mo = popt_m[0]*x**-popt_m[1]
#print(power_mo)

popt_y, pcov_y = curve_fit(lambda fx,a,b: a*fx**-b, x, y_yr)
power_yr = popt_y[0]*x**-popt_y[1]
#print(power_yr)

# add trendlines, hide as necessary
plt.plot(x, power_day, color = "black", linewidth = 1, linestyle = "--")
plt.plot(x, power_mo, color = "black", linewidth = 1, linestyle = "--")
plt.plot(x, power_yr, color = "black", linewidth = 1, linestyle = "--")

# legend, change as necessary
#plt.legend(['Frequency - Days', 'Frequency - Month', 'Frequency - Year', 'power fit'])
plt.legend()
#plt.annotate('R**2', power_yr, xy=(0.05, 0.95), xycoords='axes')
#plt.annotate("r-squared = {:.3f}".format(r2_score(y_test, y_predicted)), (0, 1))
#plt.annotate("r-squared = {:.3f}".format(r2_score(y_test, y_predicted)), (0, 1))
#plt.annotate("r-squared = {:.3f}".format(r2_score(y_test, y_predicted)), (0, 1))

# display
plt.show()