# -*- coding: utf-8 -*-

########################################################
#
#        ISS LIS Lightning Flash Heat Map and Flash Location 
#        CSV File
#	
#        Decription: This code pulls ISS LIS NetCDF data files 
#        from a directory, extracts the flash coordinates from 
#        the files and generates a flash heat map plot. This code 
#        also compiles all lightning flash locations into a single 
#        CSV file, so they may be plotted using other software
# 
#        Authors: Amanda Weigel
#        Information and Technology Systems Center (ITSC)
#        University of Alabama in Huntsville
#        
#        Last Edit Date: 02 February 2018
#
########################################################

#### Import Python packages ####
import numpy as np
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import csv
from itertools import izip


#Define the file directories
dataDir = 'C:/Users/AWeigel/Documents/ScienceOutreach/Masthead/Masthead_Jan/isslis_swath_0104/' #File path where ISS LIS data are stored
csvfile = "C:/Users/AWeigel/Documents/ScienceOutreach/Masthead/Masthead_Jan/isslis_01042918_flashloc_test.csv" #File path and name of CSV file

#Identify all NetCDF files in the directory
files = glob.glob(dataDir+'*.nc')

#Create empty arrays to populate lightning flash location coordinates 
flash_lat = np.array([]) #latitude
flash_lon = np.array([]) #longitude


#Loop through list of NetCDF files, for each file, extract the lightning flash latidude
#and longitude, and add to the respective empty array (flash_lat and flash_lon)
for i in files:
    datafile = Dataset(i)
    
    flash_lat = np.concatenate([flash_lat,datafile.variables['lightning_flash_lat'][:]]) #add to array
    flash_lon = np.concatenate([flash_lon,datafile.variables['lightning_flash_lon'][:]]) #add to array


#Create CSV files of values from the populated flash_lat/lon arrays  
with open(csvfile, 'wb') as myfile:
    writer = csv.writer(myfile)
    writer.writerows(izip(["flash_lat"], ["flash_lon"])) #Define headers in row (izip creates columns)
    writer.writerows(izip(flash_lat,flash_lon)) #Define data rows (izip creates columns)


#Create plot of lightning flash location heat map
plt.figure(figsize=((20,20))) #Set plot dimensions
map = Basemap(projection='cyl', lon_0 = 0, resolution='c')
lightning = map.hexbin(flash_lon, flash_lat, gridsize=300,bins='log',cmap='jet',mincnt=1,zorder=10) #Bin flash counts into hexbins using a gridsize of your choice

#Draw geographic boundaries and meridians/parallels
map.drawmapboundary(fill_color='k')
map.fillcontinents(color='grey',lake_color='grey')
map.drawcoastlines(color='white')
map.drawcountries(color='white')
map.drawmeridians(np.arange(0,390,30), labels=[0,0,0,1],fontsize=10, color="lightgray")
map.drawparallels(np.arange(-90,120,30), labels=[1,0,0,0],fontsize=10, color="lightgray")

cbar = map.colorbar(lightning,location='bottom',pad="5%")
cbar.set_label('Flash Count') #Remember to change label

plt.title('ISS LIS Detected Lightning Flash Locations January 4, 2018', fontsize = 18) #Rember to change title


plt.show()