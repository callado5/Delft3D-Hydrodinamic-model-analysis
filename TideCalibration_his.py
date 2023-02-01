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
from scipy import stats

# Loading Model
os.chdir('Directory') #Entering the output model directory 
ds= nc.Dataset('FileName.nc')#Loading my netCDF historical files
print(ds.variables.keys()) #Prints out my netcdf variable names
w = ds.variables['waterlevel'] [2879:-1, 0] #getting my waterlevel variable in my his, getting the first column, also droping the first 10 days of the model

#Generating a datetime variable for the model
ti = datetime.datetime(2021,4,20,0,0,0)
tf = datetime.datetime(2021,5,31,0,0,0)
dtm = datetime.timedelta(minutes=5)
tmodel = np.arange(ti,tf,dtm)

# Loading my Real Data
os.chdir('Directory_RealData')
df = pd.read_csv('WaterLevel.txt', header=None) #Loading real data

ti =datetime.datetime(2022,2,3,16,10,0) #starttime of your waterlevel data
tf=datetime.datetime(2022,2,15,15,00,0) #finaltime of your waterlevel data
dt =datetime.timedelta(minutes=10) #timestep

treal = np.arange(ti,tf,dt) #creating a datetime array that varies 10minutes (real date)

df.columns = ['LEVEL'] #Giving a name to my water level column
df.index = treal #Putting a date index on the matrix

# Interpolateion from 10 to 5 minutes

trealnew = np.arange(ti,datetime.datetime(2022,2,15,14,55,0),dtm) #creating a data array that varies in 5min

df1 = pd.DataFrame(index=trealnew) #Creating a new matriz with only the index dates that varies in 5 min
df1 = df1.join(df) # Adding my tide values to the new matrix, note that when you use the join function to interpolate the data should have the same time but a diferent timestep
df1 = df1.interpolate() # Filling the gaps (NaN)
real = df1 #giving a name to my new matrix
#################################################################################################################################################################################

# Using ttide
interval = 300/3600 # 5minutes interval
tide = t_tide(w, dt=300/3600, stime = datetime.datetime(2021,4,30,0,30,0),lat=0.1) #getting my tide harmonic tides
#print(tide.keys()) #Return the output of my ttide
modelresult = tt.t_predic(trealnew,tide['nameu'],tide['fu'],tide['tidecon'], lat =0.1) # using ttide to predict the model

#Saving my ttide sumary
sumary = pd.DataFrame()
sumary['Harmonic'] = tide['nameu']# saving tide
sumary['Amplitude'] = tide['tidecon'] [:,1]
sumary['Phase'] = tide['tidecon'] [:,2]
print(sumary)
#np.savetxt(r) #here you can export it to a txt file

#Errors RMSE
rmse = mean_squared_error(real['LEVEL'],modelresult, squared=False) #RMSE
h = np.max(modelresult)-np.min(modelresult) #Normalization to get the error%
error = rmse*100/h #the percentege difference of the curves

#Printing the diference between the model and the observed data and returning if my model is satisfied <10%
if error<=10:
    print('Error below the limit, acurate model:', error,'%')
else:
    print('Error above the limit, model not satisfied', error,'%')

# Plotting the observed and model data
plt.plot(trealnew, modelresult, 'k')
plt.plot(trealnew, real['Nivel'])
plt.legend(['Modelo', 'Real'])
plt.show()

#################################################################################################################################################################################

#Linear Regression
x = modelresult
y = real['LEVEL']
slope, intercept, r, p, std_err = stats.linregress(x, y) #getting the curvefitting sumary and the r correlation (Pearson)

def myfunc(x):
  return slope * x + intercept #Defining the function of the linear regression 

#Nash Sutcliff (Model eficiency) > NSE
def NSE(x,y):
  return (1-(np.sum((y-x)**2)/np.sum(x-np.mean(y))**2))

#Pearson Correlation
def Pearson(x,y): #We already have the pearson correlation as the r of the curve fitting status, but i use this to not forget to define pearson
  return np.corrcoef(x,y)

Nash_Sutcliff = NSE(x,y)
p= Pearson(x,y)
lfit = list(map(myfunc, x)) #Regression function curve, y = a.x + b >> myfunc = slope*x+intercept

#Plotting the linear regression
plt.figure(figsize=(8, 6), dpi=100)
plt.plot(x, lfit, '#0b7570')
plt.scatter(x, y, facecolor = 'none', edgecolors='#e8e03f')
plt.title('Linear Regression')
plt.xlabel('Model')
plt.ylabel('Observed')
plt.show()

print('Pearson:',r)
print('Nash Sutcliff:',Nash_Sutcliff)
