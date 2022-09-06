#################################################################################
#
# LANCE NRT AMSR2 Ocean Rain Data Quickview
#
# Description: This code reads latitudes, longitudes, and surface
# precipitation rates from a LANCE NRT AMSR2 Ocean Rain Data file (*.he5)
# and generate a CSV file with these info. The CSV file will be used to
# plot surface precipitation rates in ESRI ArcMap.
#
# Authors: Lucy Wang, Leigh Sinclair,
# Information and Technology Systems Center (ITSC)
# University of Alabama in Huntsville
#
# Last Edit Date: 31 January 2019
#
##################################################################################

import numpy as np
import tables
import csv

#Define the file directories
dataDir = 'C:/users/lwang/documents/projects/AMSR2_DataRecipe/'
files = ['AMSR_2_L2_RainOcean_R00_201812312341_D.he5']
datafiles = [dataDir + x for x in files]

#Create a list of dictionaries 'dict_list'; each dictionary has three keys 'lon', 'lat', 'sfc_precip'
dict_list = []
fieldnames = ['lon','lat','sfc_precip']

#Loop through list of HDF-EOS5 files, for each file, extract the surface precipitation
# and correspoinding latitude and longitude 
for i in datafiles:
    #Open HDF5 file
    h5file = tables.open_file(i)

    #Read data layer(s) of interest within HDF-EOS5 file
    surface_precip = h5file.get_node('/HDFEOS/SWATHS/GPROF2010V2/Data Fields/surfacePrecipitation').read()
    quality_flag = h5file.get_node('/HDFEOS/SWATHS/GPROF2010V2/Data Fields/QualityFlag').read()
    pixel_status = h5file.get_node('/HDFEOS/SWATHS/GPROF2010V2/Data Fields/pixelStatus').read()
    lat = h5file.get_node('/HDFEOS/SWATHS/GPROF2010V2/Geolocation Fields/Latitude').read()
    lon = h5file.get_node('/HDFEOS/SWATHS/GPROF2010V2/Geolocation Fields/Longitude').read()

    #Close HDF5 file
    h5file.close()

    n_track = surface_precip.shape[0]
    n_xtrack = surface_precip.shape[1]

    for ii in range(0,n_track):
        for jj in range(0,n_xtrack):
            if pixel_status[ii,jj] == 0 and quality_flag[ii,jj] == 0 and surface_precip[ii,jj] > 0:
               #Create a new dictionary with the three keys 'lon', 'lat', 'sfc_precip'
               row_dict = {}
               row_dict.update({'lon':lon[ii,jj],'lat':lat[ii,jj],'sfc_precip':surface_precip[ii,jj]})

               #Add this new dictionary to the list
               dict_list.append(row_dict)

#write lon, lat, surface_precip into a CSV file
if len(dict_list) > 0:
   output_csv_file = dataDir + 'AMSR2_NRT_L2B_swath_20181231.csv'
   
   with open(output_csv_file,'wb') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(dict_list)
