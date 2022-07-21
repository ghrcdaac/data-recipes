# -*- coding: utf-8 -*-
########################################################
#
#        HS3 HIWRAP Quickview
#	
#        Decription: This code pulls HS3 HIWRAP data from the GHRC 
#        OPeNDAP to generate a 2-panel time-height vertical
#        cross-section plot of radar reflectivity (dBZ).
# 
#        Authors: Amanda Weigel, Srirksha Nagaraj, 
#        Information and Technology Systems Center (ITSC)
#        University of Alabama in Huntsville
#        
#        Last Edit Date: 06 March 2018
#
########################################################

##Import python packages and modules
import pydap
from pydap.client import open_url
import numpy as np
import matplotlib 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import date, datetime, timedelta


##Set Parameters (OPeNDAP path, font and label size)
#Set the GHRC OPeNDAP file path
datafile = open_url('https://ghrc.nsstc.nasa.gov:443/opendap/fieldCampaigns/hs3/HIWRAP/data/2013/0915/HS3_HIWRAP_20130915_kainnerchirp_183446-191457_v02.nc')

#Set label size for entire plot
pltlbl_size = 12

#Set font size for entire plot
matplotlib.rcParams.update({'font.size': 10})


##Convert the time format to UTC
datetime_format = '%Y-%m-%d%H:%M:%S'
date_format = '%d%b%y'
time_format = '%H:%M:%S'
unit_string = datafile['time'].units.replace("seconds since ","").replace("T", "").replace("Z", "")
reference_time =  datetime.strptime(unit_string, datetime_format)
reference_date =  reference_time.date()

#Extract the range and time information from the datafile
var_range = datafile['range'][:] #range
var_time = datafile['time'][:] #time

timearray=[] #Empty list of converted time information
#Extracting the time from the  time data variable
for i in range(0 , (var_time.size - 1)):
       time_value = var_time[i].item()
       timearray.append((reference_time + (timedelta(seconds = time_value))).time())


##Format time and range information for creating a 2 panel plot
timearray = np.array(timearray) #Convert extracted time variables to a numpy array
var_time = np.array(var_time) #Convert to numpy array
var_range = np.array(var_range) #Convert to numypy array
nrows =  var_time.size/2
ncols =  var_range.size
first_half = (var_time.size)/2 #Split extracted time range in half to use between two plot panels

if(var_time.size %2 == 0):
    #Get 'ATB_dbZ' variable as var_dBz
    var_dBZ_first = datafile['ref'][0:first_half,:] #Extract reflectivity variable, 1st half
    var_dBZ_first = np.array(var_dBZ_first) #Convert to numpy array
    grid = var_dBZ_first.reshape((nrows, ncols)) #Grid array
    var_dBZ_second =  datafile['ref'][first_half:,:] #Extract reflectivity variable, 2nd half
    var_dBZ_second = np.array(var_dBZ_second) #Convert to numpy array
    grid_second = var_dBZ_second.reshape((nrows, ncols)) #Grid array
   
else:
    var_dBZ_first = datafile['ref'][0:first_half,:] #Extract reflectivity variable, 1st half
    var_dBZ_first = np.array(var_dBZ_first) #Convert to numpy array
    grid = var_dBZ_first.reshape((nrows, ncols)) #Grid array
    var_dBZ_second =  datafile['ref'][first_half:,:] #Extract reflectivity variable, 2nd half
    var_dBZ_second = np.array(var_dBZ_second) #Convert to numpy array
    grid_second = var_dBZ_second.reshape((nrows+1, ncols)) #Grid array
         
#Format the x-axis parameter according to the requirements of matplotlib
x_lims = []  #Create empty array for formatted x-axis information
  
for i in range(0, timearray.size): 
    x_lims.append(datetime.combine(reference_date, timearray[i]))
x_lims = [matplotlib.dates.date2num(i) for i in x_lims]


## Create a stacked 2 panel time-height plot of dBZ
fig, (ax, ax2) = plt.subplots(2, 1)

#Format ticks
ax.xaxis_date()
date_format = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(date_format) 
ax2.xaxis_date()
ax2.xaxis.set_major_formatter(date_format)

cmap = cm.get_cmap('gist_ncar', 256) #Set plot colormap

#Set up each panel plot (top and bottom plots)
dBZ_first=ax.imshow(grid.T, extent=[x_lims[0], x_lims[nrows] , var_range.min(), var_range.max()],
           interpolation='nearest', vmin=-10, vmax=50, cmap=cmap ,aspect= 'auto')
dBZ_second=ax2.imshow(grid_second.T, extent=[x_lims[nrows+1], x_lims[-1] , var_range.min(), var_range.max()],
              interpolation='nearest', vmin=-10, vmax=50, cmap=cmap ,aspect= 'auto')

#Set axis labels. The pltlbl_size variable is set at the begining of the code
ax.set_ylabel('Height (m)', fontsize=pltlbl_size) #Top y-axis label
ax2.set_xlabel('UTC Time (HH:MM:SS)', fontsize=pltlbl_size) #Bottom x-axis label
ax2.set_ylabel('Height (m)', fontsize=pltlbl_size) #Bottom y-axis label
ax.set_title('HS3 HIWRAP Attenuated Backscatter Profile', fontsize=14) #Plot title. Manually change font size.


##Plot the colorbars
#Top color bar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="4%", pad=0.2)
cbar = plt.colorbar(dBZ_first,cax=cax)
cbar.set_label('dBZ') #Remember to change label
#cbar.set_label('dBZ', fontsize=10) #Use if you'd like to manually change labels
#cbar.ax.tick_params(labelsize=10) 

#Bottom color bar
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="4%", pad=0.2)
cbar2 = plt.colorbar(dBZ_second,cax=cax2)
cbar2.set_label('dBZ') #Remember to change label
#cbar2.set_label('dBZ', fontsize=10) #Use if you'd like to manually change labels
#cbar2.ax2.tick_params(labelsize=10)

plt.show()



