"""
Show the current drawn from the tool on the LCD screen.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
from scipy.signal import butter, lfilter, freqz


def df_normalize(df):
    normalized_df=(df-df.min())/(df.max()-df.min())
    return normalized_df

def findslope(xi,xf,yi,yf):
    slope=(yf-yi)/(xf-xi)
    return slope


sample_rate=119

# Input Current Data
plt.close('all')
filename ='/Users/josebendana/Desktop/SmartTools/Current_Test1661960649.csv'
data = pd.read_csv(filename)
time=data['Time']
Isens=data['Isens']


#Scale the current data    
Isens_scaled=df_normalize(Isens)

# Rolling average
rolling_window=100
Isens_rolling=Isens_scaled.rolling(rolling_window).mean()

#Calculate "instantaneous" slope of the Isens SMA curve
slope=[]
for i in range(0,len(Isens_rolling)-1):
    slope.append(findslope(time[i],time[i+1],Isens_rolling[i],Isens_rolling[i+1]))
slope.append(slope[len(slope)-1]) #Copy the last value and add to make time and slope lists == len

#SMA of slope
slope_df=pd.DataFrame(slope)
rolling_window=100
slope_df_rolling=slope_df.rolling(rolling_window).mean()
slope_df_rolling=slope_df_rolling.squeeze()


#--------------Identify tool start times---------------------------       
start_ll=0.05
slope_start_ll=.02
start_x=[]
start_y=[]
for i in range(0,len(Isens_rolling)):
    # Check if current is crossing upward through tool start limit
    # If true, record x & y and add to list
    if Isens_rolling[i] > start_ll and Isens_rolling[i-1] < start_ll:
        x=time[i]
        y=Isens_rolling[i]
        # Due to SMA lag, crossover point is adjusted
        # Scan one second back from cross over point
        # If the slope becomes positive (> slope _start_ll) save point as new x y
        # Shift x (rolling_window/50) to account for SMA lag of slope
        s_scan=int((x-1)*sample_rate)
        e_scan=int(x*sample_rate)
        for i in range(s_scan,e_scan):
              if slope_df_rolling[i] > slope_start_ll and slope_df_rolling[i-1] < slope_start_ll:
                  a_x=time[i-rolling_window/50]
                  a_y=Isens_rolling[i-rolling_window/50]
                  start_x.append(a_x)
                  start_y.append(a_y)


#--------------Identify tool stop times---------------------------  
stop_ll=0.2
slope_stop_ll=-0.02
stop_x=[]
stop_y=[]
for i in range(0,len(Isens_rolling)):
    # Check if current is crossing downward through tool start limit
    # If true, record x & y and add to list
    # Due to SMA lag, crossover point is adjusted
    # Subtract time period (rolling_window/2) to shift point lefward
    if Isens_rolling[i] < stop_ll and Isens_rolling[i-1] > stop_ll:
        x=time[i-rolling_window/2]
        y=Isens_rolling[i-rolling_window/2]
        stop_x.append(x)
        stop_y.append(y)

# #--------------Identify work start times---------------------------       
start_ll=0.3
slope_start_ll=.025
w_start_x=[]
w_start_y=[]
for i in range(0,len(Isens_rolling)):
    # Check if current is crossing upward through tool work limit
    # If true, record x & y and add to list
    if Isens_rolling[i] > start_ll and Isens_rolling[i-1] < start_ll and Isens_rolling[i-int(.25*sample_rate)] > 0.1:
        x=time[i]
        y=Isens_rolling[i]
        # Due to SMA lag, crossover point is adjusted
        # Scan one second back from cross over point
        # If the slope becomes positive (> slope _start_ll) save point as new x y
        # Shift x (rolling_window/50) to account for SMA lag of slope
        s_scan=int((x-1)*sample_rate)
        e_scan=int(x*sample_rate)
        for i in range(s_scan,e_scan):
              if slope_df_rolling[i] > slope_start_ll and slope_df_rolling[i-1] < slope_start_ll:
                  a_x=time[i-rolling_window/50]
                  a_y=Isens_rolling[i-rolling_window/50]
                  w_start_x.append(a_x)
                  w_start_y.append(a_y)


# #--------------Identify work stop times---------------------------       
stop_ll=0.34
slope_start_ll=-0.005
w_stop_x=[]
w_stop_y=[]
for i in range(0,len(Isens_rolling)):
    # Check if current is crossing upward through tool work limit
    # If true, record x & y and add to list
    if Isens_rolling[i] < stop_ll and Isens_rolling[i-1] > stop_ll and Isens_rolling[i-int(1.5*sample_rate)] > 0.05:
        x=time[i]
        y=Isens_rolling[i]       
        # Due to SMA lag, crossover point is adjusted
        # Scan one second back from cross over point
        # If the slope becomes negative (< slope _start_ll) save point as new x y
        # Shift x (rolling_window/50) to account for SMA lag of slope
        s_scan=int((x-1)*sample_rate)
        e_scan=int(x*sample_rate)
        for i in range(s_scan,e_scan):
              if slope_df_rolling[i] < slope_start_ll and slope_df_rolling[i-1] > slope_start_ll:
                  a_x=time[i-rolling_window/50]
                  a_y=Isens_rolling[i-rolling_window/50]
                  w_stop_x.append(a_x)
                  w_stop_y.append(a_y)



# plt.figure(1)
# plt.plot(time,Isens_scaled,label="Raw",zorder=0,linewidth=0.5)
# plt.plot(time,Isens_rolling,'black',label="SMA",zorder=1)
# plt.plot(time,slope_df_rolling,label="Slope SMA",c="m",zorder=0)
# plt.scatter(start_x,start_y,marker="o",c="lime",zorder=4,linewidth=2) 
# plt.scatter(stop_x,stop_y,marker="o",c="r",zorder=4,linewidth=2)
# plt.scatter(w_start_x,w_start_y,marker="^",c="lime",zorder=4,linewidth=2)
# plt.scatter(w_stop_x,w_stop_y,marker="v",c="r",zorder=4,linewidth=2)




# #---------------------------Performance Calculations--------------------------
# Tool Start/Stop
start_x=pd.DataFrame(start_x)
start_y=pd.DataFrame(start_y)
stop_x=pd.DataFrame(stop_x)
stop_y=pd.DataFrame(stop_y)
ss_df=pd.concat([start_x,start_y,stop_x,stop_y],axis=1)
ss_df.columns=['start_x','stop_y','stop_x','stop_y']





# Work Start/Stop

w_start_x=pd.DataFrame(w_start_x)
w_start_y=pd.DataFrame(w_start_y)
w_stop_x=pd.DataFrame(w_stop_x)
w_stop_y=pd.DataFrame(w_stop_y)
w_ss_df=pd.concat([w_start_x,w_start_y,w_stop_x,w_stop_y],axis=1)
w_ss_df.columns=['w_start_x','w_stop_y','w_stop_x','w_stop_y']





# print("Total Work Time: {0:.2f}".format(len(time)/sample_rate))
tool_on=[]
for i in range(0,len(ss_df)):
    t_start=ss_df.iloc[i,0]
    t_end=ss_df.iloc[i,2]
    t_pass=t_end-t_start
    tool_on.append(t_pass)
    


work_on=[]
for i in range(0,len(w_ss_df)):
    t_start=w_ss_df.iloc[i,0]
    t_end=w_ss_df.iloc[i,2]
    t_pass=t_end-t_start
    work_on.append(t_pass)
    




print("Total Sample Time: {0:.2f}".format(len(time)/sample_rate))
print("Total Tool On Time: {0:.2f}".format(sum(tool_on)))
print("Total Work Time: {0:.2f}".format(sum(work_on)))
print("Average Time per Pass: {0:.2f} \n".format(sum(work_on)/len(work_on)))


# for i in range(0,len(ss_df)):
#     print("Tool Start # {}".format(i))
#     print("Time elapsed: {0:.2f} s \n".format(len(tool_on)))

# # for i in range(0,len(w_ss_df)):
# #     print("Routing Pass # {}".format(i+1))
# #     print("Time elapsed: {0:.2f} s \n".format(t_pass))











