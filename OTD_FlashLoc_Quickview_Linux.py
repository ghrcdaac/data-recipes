#!/usr/bin/env python3

########################################################
#
#        OTD Lightning Flash Heat Map and Flash Location 
#        CSV File for Linux
#	
#        Decription: This code pulls OTD HDF data files 
#        from a directory, decompressed the files, extracts the 
#        flash coordinates from the files and generates a flash 
#        heat map plot. This code also compiles all lightning 
#        flash locations into a single CSV file, so they may 
#        be plotted using other software.
# 
#        Authors: Amanda Markert and Essence Raphael
#        Information and Technology Systems Center (ITSC)
#        University of Alabama in Huntsville
#        
#        Last Edit Date: 06 January 2020
#
########################################################

#### Import Python Packages ####
import sys
import glob
import os
import tarfile
import subprocess
import re
from pyhdf.HDF import *
from pyhdf.VS import *
import numpy as np
import datetime
import csv
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#Initial file path. It can be changed by passing a different path as an argument
#to the main() function
file_path = 'D:/data_recipes/otd/'

def main(file_path):

    #Define the data directoy and identify the .tar files inside the data directory
    dataDir = os.path.join(file_path, '')
    raw_tar_files = glob.glob(dataDir+'otdlip_*_daily.tar')
    tfiles = [os.path.normpath(i) for i in raw_tar_files]

    #Extract earliest and latest dates from "tfiles" to create directory names
    #Create empty list to hold dates and loop through each .tar to extract the date from its filename
    file_dates = []
    for i in tfiles:
        file_dates.append(re.findall('(\d+\.\d+)', i))
    
    #Select the maximum and minimum dates
    file_dates_start = min(file_dates)
    file_dates_end = max(file_dates)

    #Create a new folder to hold the untarred data files
    if file_dates_start != file_dates_end:
        os.mkdir(os.path.normpath(dataDir+'otd_' + file_dates_start[0] + '_' + file_dates_end[0] + '_untarred_daily'))
        untar_dataDir = os.path.join(file_path, 'otd_' + file_dates_start[0] + '_' + file_dates_end[0] + '_untarred_daily/')
    else:
        os.mkdir(os.path.normpath(dataDir+'otd_' + file_dates_start[0] + '_untarred_daily'))
        untar_dataDir = os.path.join(file_path, 'otd_' + file_dates_start[0] + '_untarred_daily/')

    #Untar and extract all files contained within each .tar file
    for i in tfiles:
        with tarfile.TarFile(i, 'r') as tar_files:
            tar_files.extractall(untar_dataDir)

    #Identify the .Z files inside the untarred files data directory
    raw_untarred_files = glob.glob(untar_dataDir+'mlab.otd.1_1.*.Z')
    untarred_files = [os.path.normpath(i) for i in raw_untarred_files]
     
    #Decompress the .Z files 
    for i in untarred_files:
        subprocess.call(['uncompress', i])
                           
    #Identify the OTD HDF files in the directory
    raw_files = glob.glob(untar_dataDir+'mlab.otd.1_1.*')
    files = [os.path.normpath(i) for i in raw_files]   
       
    #Create empty numpy arrays to hold the flash latitudes, longitudes, and occurence times
    flash_lats = np.array([])
    flash_lons = np.array([])
    times = np.array([])

    #Loop through, rename and read each OTD HDF file
    for i in files:
        vs_file = HDF(i, HC.READ).vstart()
        
        #Define the location of the lightning flash coordinates in the HDF files using reference numbers 
        flash_flash = vs_file.attach(14)

        #Store the number of flash records in a variable to use when reading the data from the
        #HDF file
        flash_inquire = flash_flash.inquire()
        record_count = flash_inquire[0]

        #Create a numpy array of the flash records that have been read 
        flash_records = flash_flash.read(record_count)

        #Loop through each flash record. Extract the latitude, longitude, and occurence time for each 
        #flash. For each flash, add its latitude, longitude, and occurence time to the "flash_lats",
        #"flash_lons", and "times" respectively.
        for i in flash_records:
            flash_lats = np.concatenate((flash_lats, i[8][0]), axis=None)
            flash_lons = np.concatenate((flash_lons, i[8][1]), axis=None)
            times = np.concatenate((times, i[1]), axis=None)

    #This section extracts and formats the flash occurence times
    #Identify the earliest and latest flash timestamps in the "times" array
    start_seconds = min(times)
    end_seconds = max(times)

    #Define the units for the start and end times then convert these times 
    #(seconds since 1993-01-01 00:00:00.000) to dates
    x = datetime.datetime(1993,1,1)
    start_date = x + datetime.timedelta(seconds=start_seconds)
    end_date = x + datetime.timedelta(seconds=end_seconds)

    #Create numerical and text date & time strings to use in filenames and the flash heat map title
    start_date_txt = start_date.strftime("%B %d, %Y")
    end_date_txt = end_date.strftime("%B %d, %Y")
    start_int = start_date.strftime("%Y%m%d")
    end_int = end_date.strftime("%Y%m%d")
    start_time = start_date.strftime("%X")
    end_time = end_date.strftime("%X")

    #Create CSV file and destination
    if start_int != end_int:
        csvfile = os.path.join(dataDir, 'otd_'+ start_int + '_' + end_int + '_flashloc.csv')
    else:
        csvfile = os.path.join(dataDir, 'otd_'+ start_int + '_flashloc.csv')

    #Create csv file
    with open(csvfile, 'w', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(zip(["flash_lat"], ["flash_lon"])) #Define headers in row (zip creates columns)
        writer.writerows(zip(flash_lats,flash_lons)) #Define data rows (zip creates columns)

    #Create plot of lightning flash location heat map
    plt.figure(figsize=((20,20))) #Set plot dimensions
    map = plt.axes(projection=ccrs.PlateCarree(central_longitude=0.0))
    gl = map.gridlines(crs=ccrs.PlateCarree(central_longitude=0.0), draw_labels=True, linewidth=0.8, alpha=0.5, color='white', linestyle='--')
    lightning = map.hexbin(flash_lons, flash_lats, gridsize=300, bins='log',cmap='jet', mincnt=1 ,zorder=10) #Bin flash counts into hexbins using a gridsize of your choice

    #Draw geographic boundaries and meridians/parallels
    map.set_extent([-180, 180,-90, 90])
    map.coastlines(color='white')
    map.add_feature(cfeature.LAND, facecolor='gray')
    map.add_feature(cfeature.BORDERS, edgecolor='white')
    map.add_feature(cfeature.OCEAN, facecolor='black')
    gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0 ,30, 60, 90])
    gl.xlocator = mticker.FixedLocator([-180, -150, -120, -90, -60, -30, 0 ,30, 60, 90, 120, 150, 180])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabels_top=False
    gl.ylabels_right=False
    
    #Create colorbar
    cbar = plt.colorbar(lightning, orientation='horizontal', pad=0.02, aspect=50) 
    cbar.set_label('Flash Count', fontsize=12) #Remember to change label
        
    #Create plot title based on file dates and times
    if start_date_txt != end_date_txt:
        plot_title = 'OTD Detected Lightning Flash Locations ' + start_date_txt + ' ' + start_time + ' - ' + end_date_txt + ' ' + end_time
        plt.title(plot_title, fontsize = 18)
        
        #Save the plot as an image
        plt.savefig(os.path.join(dataDir, 'otd_' + start_int + '_' + end_int +'_flashloc_plot.png'), bbox_inches='tight') 
        
    else:
        plot_title = 'OTD Detected Lightning Flash Locations ' + end_date_txt + ' ' + start_time + ' - ' + end_time
        plt.title(plot_title, fontsize = 18) 
   
        #Save the plot as an image
        plt.savefig(os.path.join(dataDir, 'otd_' + start_int +'_flashloc_plot.png'), bbox_inches='tight')  

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        main(file_path)