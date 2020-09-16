# -*- coding: utf-8 -*-
"""
Writen By Richard Bryce in the Power System Engineering Center for the National Renewable Energy Laboratory
"""

####Dummy Data#########################################################################
#######################################################################################
# Load Time Series for Load
Load_timeseries=pd.DataFrame(np.zeros((Timesteps,2),float))
Load_timeseries.columns=['Load','index_']
Load_timeseries.index_=Load_timeseries.index
Load_timeseries.Load=np.cos(Load_timeseries.index_*(2*math.pi)/24)+2
Load_timeseries=Load_timeseries.drop(["index_"],axis=1)
#convert time series to array
np.random.seed(11)    
Load_timeseries=pd.DataFrame(Load_timeseries.values*15+(np.random.rand(Timesteps,1)-1)*5)


# Load Time Series for PV Generation
PV_timeseries=pd.DataFrame(np.zeros((Timesteps,2),float))
PV_timeseries.columns=['PV','index_']
PV_timeseries.index_=PV_timeseries.index
PV_timeseries.PV=np.sin(PV_timeseries.index_*(2*math.pi)/(24*2))**2
PV_timeseries=PV_timeseries.drop(["index_"],axis=1)
#convert time series to array
np.random.seed(10)    
PV_timeseries=pd.DataFrame(PV_timeseries.values*20-(np.random.rand(Timesteps,1)-1)*10)

#######################################################################################

def BTM_Sizing(Interations,Timesteps,Time_Resolution,Load_timeseries,PV_timeseries):
   
    import pandas as pd
    import numpy as np
    import os
    import sys 
    import site
    from os.path import basename
    import math
    from scipy.optimize import linprog

    for N in range(Interations): 
          
        energy_price=2.00
        
        ##############################################################
        #Define Battery Size [kWh]
        E_Capacity=N**2   #means 24kWh
        E_Initial=E_Capacity/2    #Starting energy
        E_End=E_Capacity/2 
        PowerRatio=4  #means 4kWh/1kW
        
        ##############################################################
        # Load Time Series for Load  
        Load_array=Load_timeseries.values
        PV_array=PV_timeseries.values       
        Load_basis= Load_array-PV_array
                
        ##############################################################
        #cost coefficients, planning to minimize load imports
        c=np.append(energy_price*np.ones((1,Timesteps),float),-1*energy_price*np.ones((1,Timesteps),float),axis=1)
              
        #Build inequality Constraint Matrices
        A_ub=[]
        b_ub=[]      
        
        #build charging subset of inequality matrix
        charging_Aub_subset=np.zeros((Timesteps,2*Timesteps),float)
        for j in range(Timesteps):
            for i in range(Timesteps):
                if i == j:
                    charging_Aub_subset[i,j]=1
                elif i>j:
                    charging_Aub_subset[i,j]=1
        for j in range(Timesteps):
            for i in range(Timesteps):
                if i > j:
                    charging_Aub_subset[i,j+Timesteps]=-1
        charging_bub_subset=(E_Capacity-E_Initial)*np.ones((Timesteps,1),float)
        
        #build dischargin subset of inequality matrix
        discharging_Aub_subset=np.zeros((Timesteps,2*Timesteps),float)
        for j in range(Timesteps):
            for i in range(Timesteps):
                if i >= j:
                    discharging_Aub_subset[i,j+Timesteps]=1
        for j in range(Timesteps):
            for i in range(Timesteps):
                if i > j:
                    discharging_Aub_subset[i,j]=-1
        discharging_bub_subset=(E_Initial)*np.ones((Timesteps,1),float)
        
        #Build Load Relation subet of inequality matrix
        relation_Aub_subset=np.zeros((Timesteps,2*Timesteps),float)
        for j in range(Timesteps):
            for i in range(Timesteps):
                if i==j:
                    relation_Aub_subset[i,j]=-1
                    relation_Aub_subset[i,j+Timesteps]=1
        relation_bub_subset=Load_basis
        
        #complete A and b inequality matricies
        A_ub=np.append(np.append(charging_Aub_subset,discharging_Aub_subset,axis=0),relation_Aub_subset,axis=0)
        b_ub=np.append(np.append(charging_bub_subset,discharging_bub_subset,axis=0),relation_bub_subset,axis=0)
        
        ######################################################
        
        #Build cyclyic equality Matrix
        A_eq=np.ones((1,Timesteps*2),float)
        for i in range(Timesteps):
            A_eq[0,i+Timesteps]=-1
        b_eq=(E_End-E_Initial)*np.ones((1,1),float)
        
        ######################################################
        
        #set the storage Bounds
        bound_seq_storage= [(0,E_Capacity/PowerRatio*Time_Resolution) for i in range(Timesteps*2)]
        
        #################################################################
        #attempt to solve
        
        try:    
            res=linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bound_seq_storage, method='interior-point')
    
            Battery_Energy=np.zeros((Timesteps,1),float)
            for i in range(Timesteps):
                if i ==0:
                    Battery_Energy[i,0]=E_Initial+res.x[i]*Time_Resolution-res.x[i+Timesteps]*Time_Resolution
                else:
                    Battery_Energy[i,0]=Battery_Energy[i-1,0]+res.x[i]*Time_Resolution-res.x[i+Timesteps]*Time_Resolution
            Battery_Power=np.zeros((Timesteps,1),float)
            for i in range(Timesteps):
                Battery_Power[i,0]=res.x[i+Timesteps]-res.x[i]
            
            Net_Load_Energy_Initial=np.sum(Load_basis)*Time_Resolution
            Net_Load_Energy_Result=np.sum(Load_basis[24:-24, :]-Battery_Power[24:-24, :])*Time_Resolution
        #    Net_Load_Energy_Result=np.sum(Load_basis-Battery_Power)*Time_Resolution    
        
            if N==0:
                Result_maxtrix=np.zeros((Interations,3),float)
            Result_maxtrix[N,0]=float(N)
            Result_maxtrix[N,1]=E_Capacity
            Result_maxtrix[N,2]=Net_Load_Energy_Result     
        except:
            if N==0:
                Result_maxtrix=np.zeros((Interations,3),float)
            Result_maxtrix[N,0]=float(N)
            Result_maxtrix[N,1]=0
            Result_maxtrix[N,2]=0        
        
    #Get Optimal Size
    Results=pd.DataFrame(Result_maxtrix)
    Results.columns=['Iternation','Energy_Capacity','Total_Net_Load']
    Relative_Change=pd.DataFrame((Results['Total_Net_Load'].values[1:]-Results['Total_Net_Load'].values[:-1])/Results['Total_Net_Load'].values[:-1])
    Relative_Change = pd.DataFrame(np.zeros((1,1),float)).append(Relative_Change, ignore_index=True)
    Results['Relative_Change']=Relative_Change
    
    try:
        Optimal_Size=(Results['Energy_Capacity'].loc[Results['Relative_Change'].idxmin()]/PowerRatio,Results['Energy_Capacity'].loc[Results['Relative_Change'].idxmin()])
    except:
        Optimal_Size=(0,0)
    return(Optimal_Size)

#Execute Code 
#########################################################################3
    BTM_Sizing(Interations=21,Timesteps=168,Time_Resolution=1.0,Load_timeseries=Load_timeseries,PV_timeseries=PV_timeseries)
    