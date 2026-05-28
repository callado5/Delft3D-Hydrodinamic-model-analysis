'''
This code is used to convert a KML to LDB (Delft3D) file. 

Created by Marco Callado in 2026-05-14
Last edit: 2026-05-28

email:
mavcallado@gmail.com
'''

import geopandas as gpd
import numpy as np
from datetime import datetime

#==========================================================================#
# Opening Kml file                                                         # 
#==========================================================================#

dir = 'C:\\Users\\mavca\\Downloads\\' #Your file directory
file_name = "Sao_Caetano" #Put here your file name without its extension
epsg = 32622 #insert the epsg code for the UTM file

gdf = gpd.read_file(dir+file_name+".kml", driver='KML') #Reading your .kml file
gdf = gdf.to_crs(epsg = epsg) #Passing it to UTM (Cartesian), in Delft3D is prefered to used as cartesian coordinates

#==========================================================================#
# Creating *.ldb file                                                      # 
#==========================================================================#

f = open(file_name+'.ldb', 'w') #Opening LDB file

#Creating header
f.write("*\n")
f.write("* Landboundary created using Callado, M.A.V. code, code created in 2026-05-14,\n")
f.write(f"* File creation date: {datetime.now():%Y-%m-%d, %H:%M:%S}\n")
f.write("* more information in github: \n")
f.write("* Coordinate System = Cartesian\n")

#Getting data from my .kml file
for i, row in gdf.iterrows():

    geom = row.geometry
    nome = f"Feature_{i+1}"

    # LINESTRING                                                   

    if geom.geom_type == 'LineString':

        coord = np.array(geom.coords)

        f.write("*\n")
        f.write(f"{nome}\n")
        f.write(f"\t{coord.shape[0]}\t2\n")

        for j in range(len(coord)):
            f.write(f"\t{coord[j,0]:16.7E}\t{coord[j,1]:16.7E}\n")

    # POLYGON                                                      

    elif geom.geom_type == 'Polygon':

        coord = np.array(geom.exterior.coords)

        f.write("*\n")
        f.write(f"{nome}\n")
        f.write(f"\t{coord.shape[0]}\t2\n")

        for j in range(len(coord)):
            f.write(f"\t{coord[j,0]:16.7E}\t{coord[j,1]:16.7E}\n")

    # MULTIPOLYGON                                                 

    elif geom.geom_type == 'MultiPolygon':

        for k, poly in enumerate(geom.geoms):

            coord = np.array(poly.exterior.coords)

            f.write("*\n")
            f.write(f"{nome}_{k+1}\n")
            f.write(f"\t{coord.shape[0]}\t2\n")

            for j in range(len(coord)):
                f.write(f"\t{coord[j,0]:16.7E}\t{coord[j,1]:16.7E}\n")

f.close() #Closing ldb file

print(f"Done, {file_name}.ldb created") 
