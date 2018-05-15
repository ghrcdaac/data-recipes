# -*- coding: utf-8 -*-


##############################################################################
#
#        RSS DMSP SSM/I and SSMIS Gridded Ocean Product Quickview
#	
#        Decription: This code pulls in a GHRC RSS DMSP SSM/I and SSMIS
#        Gridded Ocean Product netCDF datafile from the GHRC OPeNDAP and 
#        creates a Python plot of the Columnar Water Vapor variable.  Please
#        note that these edits to the SSMIS data recipe are ONLY valid for
#        Python 2.7.  This will not work with Python 3.6+. 
#
#        Authors: Amanda Weigel, Christina Leach, Sriraksha Nagaraj
#        Information and Technology Systems Center (ITSC)
#        University of Alabama in Huntsville
#        
#        Last Edit Date: 10 April 2018
#
##############################################################################


# Import Python packages
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap


# Function prints each variable within the data datafile
#def show_vars(dataset):
# for v in dataset.variables:
#     print v

# Read the dataset from the GHRC OPeNDAP
dataset_url = ('https://ghrc.nsstc.nasa.gov:443/opendap/ssmis/f17/3day/data/2017/f17_ssmis_20170908v7_d3d.nc')
dataset = netCDF4.Dataset(dataset_url)
#show_vars(dataset)
    
# Extract data parameters from file
data_var = dataset["atmosphere_water_vapor_content"] # Enter name of the parameter of interest.
data_arr = data_var[:,:].data # Extract variable array
lats = dataset["latitude"][:] # Extract latitude 
lons = dataset["longitude"][:] # Extract longitide
conv_lats, conv_lons = np.meshgrid(lons, lats)


####### Account for data scales and flags #######

# Scale Factor and Quality Flags.  Note that these current values are for the variable used in this example.
scl_val = data_var.scale_factor
valdat_max = 250.0 * scl_val
valdat = data_arr < 250.0
miss_data = 251.0 * scl_val
seaice_val = 252.0 * scl_val
bad_data = 253.0 * scl_val
no_obs = 254.0 * scl_val
land = 255.0 * scl_val

# rescale arrays from internal mask to valid range
data_arr[np.where(data_arr>valdat_max)] = data_arr[np.where(data_arr>valdat_max)]* scl_val

dataset.close() # Close the dataset once desired parameters are extracted to conserve memory


####### Using the quality flag information, mask out certain areas #######

# Masks out all pixels outside the valid data range. This includes areas of missing data,
# no observations, bad data, land and sea ice. Please note that this code does not quality
# control the data.
nodata = np.ma.masked_where(data_arr <= valdat_max,data_arr) # Masks out all pixels outside the valid data range.
nodata_fill = nodata.filled(-999) # Set all values masked above equal to a single value.

#For plotting, extract areas of sea ice using the quality flag information.
seaice_mask = np.ma.masked_where(nodata > seaice_val+0.1,nodata)

#Extract data values
parameter_mask = np.ma.masked_where(data_arr > valdat_max, data_arr)


####### Plot the data #######

# Format the plot, base map and meridians
plt.figure(figsize=((20,20)))
m = Basemap(projection='cyl', lon_0 = 180, resolution='c')
m.fillcontinents(color='grey',lake_color='grey')
m.drawcoastlines()
m.drawcountries()
m.drawmeridians(np.arange(0,390,30), labels=[0,0,0,1],fontsize=10)
m.drawparallels(np.arange(-90,120,30), labels=[1,0,0,0],fontsize=10)

#Plot data variables
m.imshow(nodata_fill,cmap='binary') #Plot areas of no data.  These will appear black with this color map
m.imshow(seaice_mask,cmap='gray') #Plot areas of no data.  These will appear white with this color map
m.pcolormesh(conv_lats, conv_lons, parameter_mask, latlon=True, vmin = 0, vmax = 75, cmap = "gist_ncar") #Plot data

# Add the plot title and color bar
plt.title('RSS DMSP-F17 SSMIS 3-Day Average Ocean Columnar Water Vapor', fontsize = 22)
plt.colorbar(shrink=0.7, orientation = 'vertical', label = 'kg $m^{-2}$')


###### Add a legend ######

# Because the flag values come as an array, it was necessary to create the legend key using patches
# to define the colors seperately.
seaice_key = mpatches.Patch(edgecolor = "k", facecolor='white', label='Sea Ice')
land_key = mpatches.Patch(edgecolor = "k", facecolor='grey', label='Land')
nodata_key = mpatches.Patch(edgecolor = "k", facecolor='black', label='No Data')
plt.legend(handles=[land_key, seaice_key, nodata_key], loc=3 ) #Plot the legend in the lower left corner of the plot (loc=3)

plt.show()