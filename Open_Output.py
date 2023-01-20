import os
from time import time
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd
import ttide as tt
from ttide.t_tide import t_tide
from sklearn.metrics import mean_squared_error

# Loading Model
os.chdir('A:\Marco\Modelo_Marinha\Simulações\Sim#4 OLDDELFT(1)\DFM_OUTPUT_mare') #Entering the output model directory
ds= nc.Dataset('mare_his.nc') #Loading my netCDF historical files
#print(ds.variables.keys()) #Prints out my netcdf variable names
w = ds.variables['waterlevel'] [2879:-1, 0] #getting my waterlevel variable in my his, getting the first column

ti = datetime.datetime(2021,4,20,00,00,0)
tf = datetime.datetime(2021,5,31,00,00,0)
dtm = datetime.timedelta(minutes=5)
tmodel = np.arange(ti,tf,dtm)

# Loading my Real Data
os.chdir('A:\Marco\Modelo_Marinha\Tratamento\Dados Reais')

df = pd.read_csv('Nivel_Tratado.txt', header=None)#Loading real data


ti =datetime.datetime(2022,2,3,16,10,0) #starttime
tf=datetime.datetime(2022,2,15,15,00,0) #finaltime
dt =datetime.timedelta(minutes=10) #timestep

treal = np.arange(ti,tf,dt) #creating a data vector
trealnew = np.arange(ti,datetime.datetime(2022,2,15,14,55,0),dtm) #creating a data vector that varies in 5min

df.columns = ['Nivel'] #Giving a name to my column
df.index = treal #Putting a date index on the matrix

# Interpolateion from 10 to 5 minutes
df1 = pd.DataFrame(index=trealnew) #Creating a new matriz with only the index dates that varies in 5 min

df1 = df1.join(df) # Adding my tide values to the new matrix
df1 = df1.interpolate() # Filling the gaps 
real = df1 #giving a name to my new matrix

# Using Ttide
interval = 300/3600
tide = t_tide(w, dt=300/3600, stime = datetime.datetime(2021,4,30,0,30,0),lat=0.1) 
#print(tide.keys())
modelresult = tt.t_predic(trealnew,tide['nameu'],tide['fu'],tide['tidecon'], lat =0.1)
sumary = pd.DataFrame()
sumary['Harmonic'] = tide['nameu']# saving tide
sumary['Amplitude'] = tide['tidecon'] [:,1]
sumary['Phase'] = tide['tidecon'] [:,2]
print(sumary)
#np.savetxt(r)

#Errors RMSE
rmse = mean_squared_error(real['Nivel'],modelresult, squared=False) #RMSE
h = np.max(modelresult)-np.min(modelresult) #Normalization to get the error%
error = rmse*100/h #the percentege difference of the curves
if error<=10:
    print('Error below the limit, acurate model:', error,'%')
else:
    print('Error above the limit, model not satisfied', error,'%')

# Plot
plt.plot(trealnew, modelresult, 'k')
plt.plot(trealnew, real['Nivel'])
plt.legend(['Modelo', 'Real'])
plt.show()