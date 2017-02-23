
# coding: utf-8

# In[21]:
########################################################
#
#        SSMI Data receipe
#		Generate Data receipe  for 
#		SSMI
#
#	Author: Manil Maskey
#	Date:	Feb 23, 2017
#	Information and Technology Systems Center (ITSC)
#       University of Alabama in Huntsville
#
#
########################################################


get_ipython().magic(u'matplotlib inline')
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


# In[36]:

def show_vars(ghrc_dataset):
 for v in ghrc_dataset.variables:
     print v


# In[37]:

#Read the dataset
ghrc_dataset_url = ('https://ghrc.nsstc.nasa.gov/opendap/ssmi/f13/weekly/data/2005/f13_ssmi_20050212v7_wk.nc')
ghrc_dataset = netCDF4.Dataset(ghrc_dataset_url)
show_vars(ghrc_dataset)
    


# In[39]:

ghrc_wvc = ghrc_dataset["atmosphere_water_vapor_content"][:,:]
ghrc_lats = ghrc_dataset["latitude"][:]
ghrc_lons = ghrc_dataset["longitude"][:]
conv_lats, conv_lons = np.meshgrid(ghrc_lons, ghrc_lats)

plt.figure(figsize=((20,20)))
m = Basemap(projection='robin', lon_0 = 0, resolution='c')
m.drawcoastlines()
m.pcolormesh(conv_lats, conv_lons, ghrc_wvc, latlon=True)

plt.show()


# In[ ]:



