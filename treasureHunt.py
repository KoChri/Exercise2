__author__ = 'Christof'

# import of the needed libraries
import urllib
import h5py
import numpy as np
import netCDF4 as cdf
import os.path
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

url = "http://rs.geo.tuwien.ac.at/downloads/cpa/"
# 1
opener = urllib.URLopener()
if not os.path.isfile('table.csv'):  # checks if the file is already in the directory
    opener.retrieve(url + 'table.csv', 'table.csv')  # loads and saves the file
csv = open('table.csv')
header = csv.next().split(',')

col_index1 = header.index('candle')  # gets the index for the given string
data_csv = np.loadtxt(csv, skiprows=0,  delimiter=',', unpack=True)  # loads the csv file and skips the header

# 2
filename_nc = str(int(data_csv[col_index1][1-1])) + '_foolish.nc'
if not os.path.isfile(filename_nc):
    opener.retrieve(url + filename_nc, filename_nc)
nc_file = cdf.Dataset(filename_nc)  # loads the Dataset from the nc file

plt.figure('City')  # sets a new figure named City
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')
m.drawcoastlines()  # draws the coast lines in the given basemap
plt.imshow(nc_file.variables['force'][:], cmap='autumn_r', extent=[-180, 180, -90, 90])
# extent shifts the image to the worldmap - citie name was looked up in google maps after visualising the
# searched city on the map
part1 = 'canberra'

# 3
filename_npz = (part1 + '_mercury.npz')
col_index2 = header.index('apple')
row_npz = np.mean(data_csv[col_index2])

if not os.path.isfile(filename_npz):
    opener.retrieve(url + filename_npz, filename_npz)
data_npz = np.load(filename_npz)
filename_bin = str(int(data_npz['back'][row_npz])) + '.bin'

# 4
if not os.path.isfile(filename_bin):
    opener.retrieve(url + filename_bin, filename_bin)

bin_file = open(filename_bin)
bin_107 = bin_file.read(107)
# print bin_107  # prints the first 107 byte to see the structure of the bin, was later used in line 60-61

# 5
col_index3 = header.index('fish')
lon = data_csv[col_index3]
lat = data_npz['towel']
# reads the data von the bin file and the variable newspaper
dataset_bin = np.fromfile(bin_file, dtype=[('sunburnedpenguin', '<i2'), ('newspaper', '<i2'),
                                           ('redzebra', '<i2'), ('embarresedskunk', '<i2')])['newspaper']

filename_h5py = h5py.File('treasuremap.hdf5', 'w')  # defining and saving the hdf5 file
dataset = filename_h5py.create_dataset('treasure', data=dataset_bin)  # creates each dataset for the hdf5
longitude = filename_h5py.create_dataset('longitude', data=lon)
latitude = filename_h5py.create_dataset('latitude', data=lat)

plt.figure('Treasuremap')
m.drawcoastlines()
plt.scatter(longitude, latitude, dataset, color='red')  # simple scatterplot with the given data
plt.show()
