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


#Plot the scaled data
plt.figure(1)
plt.plot(time,Isens_scaled,label="Raw",zorder=0,linewidth=0.5)


# Rolling average
# plt.plot(time,Isens_scaled,label="Raw")
rolling_window=100
Isens_rolling=Isens_scaled.rolling(rolling_window).mean()
plt.plot(time,Isens_rolling,'black',label="SMA",zorder=1)




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
# plt.plot(time,slope)
plt.plot(time,slope_df_rolling,label="Slope SMA",c="m",zorder=0)


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
                  plt.scatter(a_x,a_y,marker="o",c="lime",zorder=4,linewidth=2) 


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
        plt.scatter(x,y,marker="o",c="r",zorder=4,linewidth=2)

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
                  plt.scatter(a_x,a_y,marker="^",c="lime",zorder=4,linewidth=2) 




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
                  plt.scatter(a_x,a_y,marker="v",c="r",zorder=4,linewidth=2) 





# # Downward cross over
# # Define limits for ending work
# work_ll=0.34
# plt.hlines(work_ll, 0, 60, colors='orange', linestyles='solid',linewidth=1)

# d_cross_over_x=[]
# d_cross_over_y=[]
# for i in range(0,len(Isens_rolling)):
#     if Isens_rolling[i] < work_ll and Isens_rolling[i-1] > work_ll :
#         d_cross_over_x.append(time[i])
#         d_cross_over_y.append(Isens_rolling[i])

# work_ll=-.005
# d_x=[]
# d_y=[]
# for j in range(0,len(d_cross_over_x)):
    
#     s_scan=(d_cross_over_x[j]-rolling_window/200)*119
#     e_scan=(d_cross_over_x[j])*119
#     # plt.vlines(s_scan/119, -0.6, 1, colors='red', linestyles='solid',linewidth=0.5)
#     # plt.vlines(e_scan/119, -0.6, 1, colors='red', linestyles='solid',linewidth=0.5)
#     s_scan=int(s_scan)
#     e_scan=int(e_scan)
#     for i in range(s_scan,e_scan):
#         if slope_df_rolling[i] < work_ll and slope_df_rolling[i-1] > work_ll  :
#             d_x.append(time[i])
#             d_y.append(Isens_rolling[i])

    
# plt.scatter(d_x,d_y,marker="x",c="r",zorder=4,linewidth=2)



# plt.title('Scaled Current vs Time')
# plt.grid( linestyle = '--', linewidth = 0.5,markevery=1)
# plt.yticks(np.arange(-.6, 1, 0.05)) 
# plt.xticks(np.arange(0, len(data)/119, 2))
# plt.legend()


# #---------------------------Performance Calculations--------------------------
# d_cox_df=pd.DataFrame(d_x)
# d_coy_df=pd.DataFrame(d_y)
# u_cox_df=pd.DataFrame(u_x)
# u_coy_df=pd.DataFrame(u_y)

# ss_df=pd.concat([d_cox_df,d_coy_df,u_cox_df,u_coy_df],axis=1)
# ss_df.columns=['d_cox_df','d_coy_df','u_cox_df','u_coy_df']

# # plt.figure(2)


# # plt.scatter(ss_df['d_cox_df'],ss_df['d_coy_df'],marker="x",c="r",zorder=4,linewidth=2)
# # plt.scatter(ss_df['u_cox_df'],ss_df['u_coy_df'],marker="x",c="g",zorder=4,linewidth=2)

# print("Total Time: {0:.2f}".format(len(time)/sample_rate))
# print("Number of Passes: {0:.2f} \n".format(len(ss_df)))
# for i in range(0,len(ss_df)):

#     t_start=ss_df.iloc[i,2]
#     t_end=ss_df.iloc[i,0]
#     t_pass=t_end-t_start
#     print("Routing Pass # {}".format(i))
#     print("Time elapsed: {0:.2f} s \n".format(t_pass))


























