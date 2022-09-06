
########################################################
#   
#    This code takes GHRC LANCE AMSR2 Snow Water Equivalent Data 
#    formatted in 25km HDF-EOS5 files, georeferences it to 
#    NSIDC Polar Grids, and creates four GeoTIFF files.
#   
#   Inputs: GHRC NRT AMSR2 Daily L3 Global Snow Water Equivalent EASE-Grids
#   Outputs: Four GeoTIFF files of North and South Pole Snow Water Equivalent
#           (SWE) and flags.
#    
#    Authors: Kel Markert (1), Amanda Weigel(2)
#
#    (1) Earth System Science Center (ESSC)    
#    (2)Information and Technology Systems Center (ITSC)
#    University of Alabama in Huntsville
#
#   Data Edited: Date: April 07, 2017
#
########################################################

import numpy
from osgeo import gdal, osr
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
<<<<<<< HEAD:old_py_recipes/Georef_AMSR2_SWE_PolarGrid_Data_Recipe.py
=======
#import osr
>>>>>>> 4eee8ad9ad6124275128bee110bbcc56db4e7928:Georef_AMSR2_SWE_PolarGrid_Data_Recipe.py
import tables
from pyproj import Proj, transform


# Path to input file
infile = 'test_files/georef/AMSR_U2_L3_DailySnow_P02_20220823.he5'

# Path to output file directory

outfolder = 'test_files/out/' # must have '/' at the end

# Open HDF5 file
h5file = tables.open_file(infile)

#Define metadata path to data layer of interest within file
north_grid_flags = h5file.get_node('/HDFEOS/GRIDS/Northern Hemisphere/Data Fields/Flags_NorthernDaily').read()
north_grid_SWE = h5file.get_node('/HDFEOS/GRIDS/Northern Hemisphere/Data Fields/SWE_NorthernDaily').read()

south_grid_flags = h5file.get_node('/HDFEOS/GRIDS/Southern Hemisphere/Data Fields/Flags_SouthernDaily').read()
south_grid_SWE = h5file.get_node('/HDFEOS/GRIDS/Southern Hemisphere/Data Fields/SWE_SouthernDaily').read()

# Close HDF5 file
h5file.close()

#Make sure data layers are listed in the same order as they appear in file
file_dict = {'NQAF':north_grid_flags,'NSWE':north_grid_SWE,'SQAF':south_grid_flags,'SSWE':south_grid_SWE}
             
products = ['NQAF','NSWE','SQAF','SSWE',]

# Set output projections
northProj = '''PROJCS["NSIDC EASE-Grid North",
    GEOGCS["Unspecified datum based upon the International 1924 Authalic Sphere",
        DATUM["Not_specified_based_on_International_1924_Authalic_Sphere",
            SPHEROID["International 1924 Authalic Sphere",6371228,0,
                AUTHORITY["EPSG","7057"]],
            AUTHORITY["EPSG","6053"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4053"]],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    PROJECTION["Lambert_Azimuthal_Equal_Area"],
    PARAMETER["latitude_of_center",90],
    PARAMETER["longitude_of_center",0],
    PARAMETER["false_easting",0],
    PARAMETER["false_northing",0],
    AUTHORITY["EPSG","3408"],
    AXIS["X",UNKNOWN],
    AXIS["Y",UNKNOWN]]'''    #NSIDC North Pole Ease-Grid
    
southProj = '''PROJCS["NSIDC EASE-Grid South",
    GEOGCS["Unspecified datum based upon the International 1924 Authalic Sphere",
        DATUM["Not_specified_based_on_International_1924_Authalic_Sphere",
            SPHEROID["International 1924 Authalic Sphere",6371228,0,
                AUTHORITY["EPSG","7057"]],
            AUTHORITY["EPSG","6053"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4053"]],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    PROJECTION["Lambert_Azimuthal_Equal_Area"],
    PARAMETER["latitude_of_center",-90],
    PARAMETER["longitude_of_center",0],
    PARAMETER["false_easting",0],
    PARAMETER["false_northing",0],
    AUTHORITY["EPSG","3409"],
    AXIS["X",UNKNOWN],
    AXIS["Y",UNKNOWN]]'''    #NSIDC South Pole EASE-Grid
    
spat_res  = 25000 #pixel spatial resolution in meters

inProj = Proj(init='epsg:4326')

# Load GDAL GeoTIFF dataset driver for dataset format
drv = gdal.GetDriverByName("GTiff")

#looping over 4 hdf data layers within each data file

for i in range(len(products)):
    #grab data from file_dict (list of data layer arrays)
    indata = file_dict[products[i]]
    #output file path using names in file_dict  
    outfile = outfolder+products[i]+'.tif'
    
    #Checks if North or South NSIDC Ease Grid pPojection applies
    #set upper left lon and lat extent dimensions for polar data
    
    #Northern Hemisphere
    if products[i][0] == 'N':
        ullon = -135 #this is an approximate value
        ullat = -86.5 #this is an approximate value
        dest_wkt = northProj
        outProj = Proj(init='epsg:3408')
    
    #Southern Hemisphere
    else:
        ullon = -45 #this is an approximate value
        ullat = 86.5 #this is an approximate value
        dest_wkt = southProj
        outProj = Proj(init='epsg:3409')
    
    #Converts coordinates from WGS 1984 (entered above) to polar grid coordinates   
    ul_x,ul_y = transform(inProj,outProj,ullon,ullat)
    
    # Create blank ouput dataset.  Set (outfile, x-dimension,,y-dimension, number of bands, data type).
    dsOut = drv.Create(outfile, indata.shape[1],  indata.shape[0], 1, gdal.GDT_Byte)
    
    # Specify and set output file's geotransform. 
    # geotransform = [upper left longitude, x-dimension resolution, x skew, upper left latitude, y skew, y-dimension resolution (usually negative)
    gt = [ul_x, spat_res, 0, ul_y, 0, -spat_res]
    dsOut.SetGeoTransform(gt)
    
    # Set output dataset projection
    dsOut.SetProjection(dest_wkt)
    
    # Write gridded swath to the output file
    bandOut=dsOut.GetRasterBand(1)
    BandWriteArray(bandOut, indata)
    
    # Release output dataset from memory
    dsOut = None
    bandOut = None 
    
#once the file GeoTIFFs have been created, pull into ArcMap and define the projection 
#as NSIDC EASE Grid North and NSIDC EASE Grid South