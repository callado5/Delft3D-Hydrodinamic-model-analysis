# Delft3D-Hydrodinamic-model-analisys
Delft3D Hydrodinamic model analisys 
Opening my netcdf output from DFlow-Fm and reading the water level file.
This script executes the calibration phase of the water level in hydrodynamics modelling, using the Nash Sutcliff, RMSE, %RMSE and Pearson to calculate the model efficiency

Here are some plot examples extrated from the output historical files 
2D plot of the model and observed Water Level 
![image](https://user-images.githubusercontent.com/47508053/216102296-d142421b-7a53-417b-8719-b7575aa3f633.png)

Linear regression between the model data and the observed data
![image](https://user-images.githubusercontent.com/47508053/216104343-42a58df0-b956-4556-bc90-bb1f3f317ab6.png)
## Load Ugrid substances
Open Ugrids Water Quality Output: It loads the substances in water quality and plot over the ugrid model without using the quickplot function of open earth tools
![image](https://github.com/callado5/Delft3D-Hydrodinamic-model-analysis/assets/47508053/9153f71b-62a2-4fdf-b1af-6c52b6a45c14)
