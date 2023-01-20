%Criando a maré apartir de um modelo existente
addpath('A:\instalaveis_programas\OET\oet_matlab');
oetsettings;

%% Carregando os FlowElements x e y do Modelo

FlowElem_xcc=nc_varget('C:\Users\lapma\Downloads\pa_ama_medio_map.nc',...
    'FlowElem_xcc'); %posicao em x
FlowElem_ycc=nc_varget('C:\Users\lapma\Downloads\pa_ama_medio_map.nc',...
    'FlowElem_ycc'); % posicao em y

%Criando xq e yq, valores que eu quero resgatar (Como se fosse OBS points).
m = load('A:\Marco\Modelo_Marinha\tide_points.txt'); %Points (lat,lon)
x = FlowElem_xcc;     y = FlowElem_ycc;    
xq = m(:,1);          yq = m(:,2);  

%Carregando o WaterLevel
    s1=nc_varget('C:\Users\lapma\Downloads\pa_ama_medio_map.nc','s1',...
        [12145 0], [760 71780]); % nivel de superficie livre, [tempoinicial, ?], [Numero de Dados(apartir do ti), Numero de Elementos]
    s1_T = s1'; clear s1;
    %%
%Gerando para cada ponto xq e yq uma interpolação de Maré
for i = 1:760 %Como o map varia em uma hora e precisamos de 32 dias pros harmonicos temos 32*24 = 760 = numero de dados
    sl_new(:,i) = griddata(x,y,s1_T(:,i),xq,yq); %interpolando nivel de água de x e y para xq e yq apartir de um griddata
end