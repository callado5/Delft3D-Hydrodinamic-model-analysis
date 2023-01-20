import os
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
import shapefile as shp
from pyproj import Proj, transform

# Loading Model
os.chdir('A:\Marco\Modelo_Marinha\Simulações\Sim#5 OLDDELFT(1)\DFM_OUTPUT_mare') #Entering the output model directory
ds= nc.Dataset('mare_map.nc') #Loading my netCDF historical files
#print(ds.variables.keys()) #Prints out my netcdf variable names
#w = ds.variables['waterlevel'] [:, 0] #getting my waterlevel variable in my his, getting the first column
#print(ds.variables.keys())
lat = ds.variables['FlowElem_xcc'] [:]
lon = ds.variables['FlowElem_ycc'] [:]
velx = ds.variables['ucx'] [63,:]
vely = ds.variables['ucy'] [63,:]
vmap = pd.DataFrame()
vmap['Lat'],vmap['Long'],vmap['u'],vmap['v'],vmap['velocity'] = lat, lon, velx, vely,(vely+velx)

inProj = Proj(init='epsg:32622')
outProj = Proj(init='epsg:4326')
x2,y2 = transform(inProj,outProj,lat,lon)

# Plotting
sf = shp.Reader("C:\\Users\\lapma\\Downloads\\shapemarinha (3)\\marinha_line.shp")
plt.figure()
plt.tricontourf(x2, y2, velx+vely)
plt.set_cmap('Greens')
#plt.quiver(x2,y2,velx,vely, scale=10, linewidth= 0)
plt.colorbar()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y, 'k')
plt.show()

