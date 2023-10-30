"""
Grab the combined csv file for train, validate and test,
separate them into example time frames and extract statistical features. 

NOTE: Old file, use process_data.py for updated code!
"""
#Import necessary toolsets
import numpy as np
import pandas as pd


#Grab csv file from directory and convert it to pandas dataframe
raw_df= pd.read_csv('TrainData_SubjectNumberIncluded.csv')


#Drop "Subject" column because it contains strings, keep "Subject Number Column"
raw_df=raw_df.drop(['Subject'], axis=1)

#The following for loop breaks the data into frames and extracts statistical features with 50% overlap

startindex = 0 
framesize = 104*10 #Frame size can be fine tuned to improve accuracy (1 sec)
numfeatures = 110 #Each feature is statistically derived from a a frame of the entire data frame
numex = (len(raw_df) // framesize)*2# Number of example frames

#Creating an empty dataframe of zeros
processed_array = np.zeros((numex, numfeatures+3))
processed_df = pd.DataFrame(processed_array)


for i in range(0,numex):
    #Define specific frame
    stopindex=startindex+framesize
    example_segment_df=raw_df.iloc[startindex:stopindex,1:15]
   
    #Code to calculate features from example segment
    stat_df=example_segment_df.agg(['min','max','mean','kurt','sem','std','var','skew','mad','sum'])
    stat_df=stat_df.transpose()
    
    #Code to extract column information for each row in stat_df and create a df for each sensor
    #Moving forward there is probably a way to use a forloop to accomplish this step
    sensor='accX'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    accX=sensor
    
    sensor='accY'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    accY=sensor
    
    sensor='accZ'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    accZ=sensor
    
    sensor='wx'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    wx=sensor
    
    sensor='wy'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    wy=sensor
    
    sensor='wz'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    wz=sensor
    
    sensor='bx'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    bx=sensor
    
    sensor='by'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    by=sensor
    
    sensor='bz'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    bz=sensor
    
    sensor='Isens'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    Isens=sensor
    
    sensor='Srms'
    sensor=stat_df.loc[sensor]
    sensor=sensor.to_frame() 
    sensor=sensor.transpose()
    Srms=sensor
    

    
    #Code to create y label column based of mode of label in example frame (activities 0,1,2,3)
    activity=example_segment_df.loc[:,'Activity']
    activity=activity.mode()
    activity=activity.loc[0]
    
    #Code to create y label column based of mode of label in example frame (subject 0,1,2,3,4)
    subject=example_segment_df.loc[:,'Subject Number']
    subject=subject.mode()
    subject=subject.loc[0]
    
    #Code to create y label column based of mode of label in example frame (Trial 0-9)
    trial=example_segment_df.loc[:,'Trial']
    trial=trial.mode()
    trial=trial.loc[0]
    
    
    #This component populates the empty data frame (processed_df) by parts related to the index (i) 
    processed_df.iloc[i,0:10]=accX
    processed_df.iloc[i,10:20]=accY
    processed_df.iloc[i,20:30]=accZ
    processed_df.iloc[i,30:40]=wx
    processed_df.iloc[i,40:50]=wy
    processed_df.iloc[i,50:60]=wz
    processed_df.iloc[i,60:70]=bx
    processed_df.iloc[i,70:80]=by
    processed_df.iloc[i,80:90]=bz
    processed_df.iloc[i,90:100]=Isens
    processed_df.iloc[i,100:110]=Srms
    processed_df.iloc[i,110]=activity
    processed_df.iloc[i,111]=subject
    processed_df.iloc[i,112]=trial
    
    startindex = stopindex - framesize//2

#This creates a title for each column in the processed data matrix
processed_df.columns=['accX_min','accX_max','accX_mean','accX_kurt','accX_sem','accX_std','accX_var','accX_skew','accX_mad','accX_sum',
                      'accY_min','accY_max','accY_mean','accY_kurt','accY_sem','accY_std','accY_var','accY_skew','accY_mad','accY_sum',
                      'accZ_min','accZ_max','accZ_mean','accZ_kurt','accZ_sem','accZ_std','accZ_var','accZ_skew','accZ_mad','accZ_sum',
                      'wx_min','wx_max','wx_mean','wx_kurt','wx_sem','wx_std','wx_var','wx_skew','wx_mad','wx_sum',
                      'wy_min','wy_max','wy_mean','wy_kurt','wy_sem','wy_std','wy_var','wy_skew','wy_mad','wy_sum',
                      'wz_min','wz_max','wz_mean','wz_kurt','wz_sem','wz_std','wz_var','wz_skew','wz_mad','wz_sum',
                      'bx_min','bx_max','bx_mean','bx_kurt','bx_sem','bx_std','bx_var','bx_skew','bx_mad','bx_sum',
                      'by_min','by_max','by_mean','by_kurt','by_sem','by_std','by_var','by_skew','by_mad','by_sum',
                      'bz_min','bz_max','bz_mean','bz_kurt','bz_sem','bz_std','bz_var','bz_skew','bz_mad','bz_sum',
                      'Isens_min','Isens_max','Isens_mean','Isens_kurt','Isens_sem','Isens_std','Isens_var','Isens_skew','Isens_mad','Isens_sum',
                      'Srms_min','Srms_max','Srms_mean','Srms_kurt','Srms_sem','Srms_std','Srms_var','Srms_skew','Srms_mad','Srms_sum',
                      'Activity','Subject Number','Trial']

  
processed_df.to_csv('10secframe_Proccessed_train_Xy_Matrix.csv')


