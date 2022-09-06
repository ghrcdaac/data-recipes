########################################################################
#
#        Infrared Global Geostationary Composite Quick View
#
#        Description: This code generates a PNG image of an Infrared 
#                Global Geostationary Composite data file
#
#        Authors: Matthew Smith, Leigh Sinclair
#        Information and Technology Systems Center (ITSC)
#        University of Alabama in Huntsville
#
#        Last Edited: 5 July 2017
#
#
########################################################################

#Import Python packages
import sys
import os
import struct
import matplotlib.pyplot as plt
 
# Define the file path to the desired date file 
<<<<<<< HEAD:old_py_recipes/IR_Global_GeoComp_QuickView_DataRecipe.py
globir="test_files/globir.22007.0120" #Place path to file here using forward slashes
=======
globir="test_files/globir.17019.0545" #Place path to file here using forward slashes
>>>>>>> 4eee8ad9ad6124275128bee110bbcc56db4e7928:IR_Global_GeoComp_QuickView_DataRecipe.py
try:
   IN=open(globir, 'rb')
except:
   print ('Error: opening file', globir)
   exit(1)
 
# Read the first 768 bytes of the file containing the header and navigation information
dataOffset=768
header=struct.unpack('<192I', IN.read(768))
 
# Extract the data parameters
lines=header[8]
elements=header[9]
arraySize=lines*elements
format="%4dB" % (arraySize)
dataOffset=header[33]   # offset to data array (bytes)
 
# Read image array into a 1D array
IN.seek(dataOffset)
array=struct.unpack(format, IN.read(arraySize))
IN.close()
 
# Set up 2D array and reshape to 2D array to plot the data
array2D=[]
for n in range(0,lines):
   array2D.append(array[n*elements:(n+1)*elements])
 
# Create a plot of the data. The generated PNG image will save to the same folder where the data file is saved.
fig=plt.imshow(array2D, cmap='gray', interpolation='none')
plt.axis('off')
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
try:
   plt.savefig(globir+".png", dpi=400, bbox_inches='tight', pad_inches=0)
except:
   print ('Error: saving figure to',globir+".png")
   exit(1)
else:
   print ('Success, saved to', globir+".png")
plt.close('all')
exit(0)

print ("Image created")
