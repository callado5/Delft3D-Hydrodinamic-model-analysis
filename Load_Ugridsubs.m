%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                     %
%        Loading DflowFM Water quality for unstructered grid          %
%                           Marco Callado                             %
%                    email: mavcallado@gmail.com                      %
%                         September - 2023                            %
%       For this script you'll need open earth tools toolbox          %       
%                                                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Loading the data status
%
%oetsettings
WAQoutput = 'deltashell.map'; %insert your *.map WAQ output filename;
struct = delwaq('open',WAQoutput);

%Loading the ugrid - netCDF
Grid = 'FlowFM_waqgeom.nc'; %Insert your WAQ unstructured grid file
G = dflowfm.readNet('FlowFM_waqgeom.nc');
Substances.Latitude  = G.face.FlowElem_x;
Substances.Longitude = G.face.FlowElem_y;

% Exemple of the substances and how it will out put my substance files
%[time,data] = delwaq('read',struct,i,0,144);% 1= IM1; 2=FeIIId;3=FeIIIpa;4=Hg;
%delwaq(read, struct, substance, layer (if 3d), time)

[time,Substances.IM1]     = delwaq('read',struct,1,0,144);      %Sediment
[time,Substances.FeIIId]  = delwaq('read',struct,2,0,144);      %Dissolved Iron
[time,Substances.FeIIIpa] = delwaq('read',struct,3,0,144);      %Al
[time,Substances.Hg]      = delwaq('read',struct,4,0,144);      %Mercury
time = datetime(time,'ConvertFrom','datenum');

%   A brief explanation of the delwaq() function
%   [TIME,DATA] = DELWAQ('read',STRUCT,SUBSTANCENR,SEGMENTNR,TSTEP) reads
%   the specified substance (0 for all), specified segment (0 for all) and
%   specified time step (0 for all) from the Delwaq HIS or MAP file. The
%   returned TIME is a MATLAB serial date if reference date and time step
%   size information is available in the file; otherwise time index
%   information is returned. The returned array is of size NSUBS x NSEGM x
%   NTIMES where NSUBS is the number of selected substances, NSEGM the
%   number of selected segments, and NTIMES the number of selected time
%   steps.
%
%   NOTE: All NaN files will be -999 as in delft3D 

clear G struct
%--------------------------------------------------------------------------%
% *NOTE:*                                                                  %
% In the after sections of the code its a treatment example to view de     %
% substance dispersion after 144 time steps of the model                   %
%--------------------------------------------------------------------------%
%% If the values are below 0.0001 then its zero
%Setting NaN
%  for i = 1:length(Substances.IM1)
%      if Substances.IM1(i) == -999 
%          Substances.IM1(i) = NaN;
%      end
%  end

% 1 has substance -1 no substance
% for i = 1:length(Substances.IM1)        
%     if Substances.IM1(i) <= 0.001
%         Substances.IM1(i) = -1; 
%     else 
%         Substances.IM1(i) = 1;
%     end
% end
% % Limit on where the substance is
%  for i = 1:length(Substances.IM1)-1
%      if (Substances.IM1(i) - Substances.IM1(i+1) == 0) %|| (Substances.IM1(i) - Substances.IM1(i+1) == 0)
%      
%      else
%          Substances.IM1(i) = 1000;
%      end
%  end 
%If it has the substance is 1 else is NaN
for i = 1:length(Substances.IM1)        
    if Substances.IM1(i) <= 0.001
        Substances.IM1(i) = NaN; 
    else 
        Substances.IM1(i) = 1;
    end
end
for i = 1:length(Substances.FeIIId)        
    if Substances.FeIIId(i) <= 0.001
        Substances.FeIIId(i) = NaN; 
    else 
        Substances.FeIIId(i) = 2;
    end
end

%% Delete all the points that has no substances and saving in a matrix
Sediment = [Substances.Latitude',Substances.Longitude',Substances.IM1'];
Sediment_cut = Sediment(sum(isnan(Sediment),2)==0,:);%deleting NaNs;

%% Ploting
%Setting a line that covers the latitude and longitude that has the points
%using the bound() function
x =Sediment_cut(:,1);
y =Sediment_cut(:,2);
bound = boundary(x,y);
pol = polyshape(x(bound),y(bound));
Arienga  = shaperead('arienga.shp');%
%
plot(x(bound),y(bound),'LineWidth',3);%Plotting only the boundary values
plot(pol, 'FaceColor','Green', 'EdgeColor','White') 
hold on
mapshow(Arienga,'FaceColor','#D3D3D3');%Gray color
grid on
ylim([9.8205*10^6 9.824*10^6]);
xlim([7.435*10^5 7.50*10^5]);
alpha(1) %transparency