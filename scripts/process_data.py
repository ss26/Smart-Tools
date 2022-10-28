"""
    Get sensor data from IMU, current sensor, microphone.
    Perform Pre-processing.
    Obtain a single pre-processed tensor.
"""
import pandas as pd
import numpy as np
import scipy as sp
import imu_file  # IMU sensor script
import current_file  # Current sensor script


def get_IMU():
    imu_data = imu_file.get_data()
    return imu_data


def get_current():
    current_data = current_file.get_data()
    return current_data

class Preprocess:
    def __init__(self):
        self._df = None
        self._axis = 0
        self._col_dict = None
        self._sensor = None
        self.sensors = ["accX", "accY", "accZ", "wx", "wy", "wz", "bx", "by", "bz", "Isens", "SRMS"]
    
    def get_statistics(self, col: np.array, sensor: str):
        """

        CREATES
            One pandas dataframe row containing the following statistics:
            - min, max
            - mean, kurtosis, sem
            - std, variance, skew
            - mad, sum
        """
        assert col.size != 0, f"Invalid size for data column: {col.size}"
        assert len(sensor) >= 0, f"No sensor type provided for data column: {sensor}"
        
        # mean absolute deviation, scipy has median
        # TODO: which to use?
        def mad(x, axis):
            return np.mean(np.absolute(x - np.mean(x, axis)), axis)
        col_dict = dict()
        col_dict["max"] = np.amax(col, axis=self._axis)
        col_dict["min"] = np.amin(col, axis=self._axis)
        col_dict["mean"] = np.mean(col, axis=self._axis)
        col_dict["kurtosis"] = sp.stats.kurtosis(col, axis=self._axis)
        col_dict["sem"] = sp.stats.sem(col, axis=self._axis)
        col_dict["std"] = np.std(col, axis=self._axis)
        col_dict["var"] = np.var(col, axis=self._axis)
        col_dict["skew"] = sp.stats.kurtosis(col, axis=self._axis)
        # col_dict["mad"] = mad(col, axis=self._axis)
        col_dict["mad"] = sp.stats.median_abs_deviation(col, axis=self._axis)
        col_dict["sum"] = np.sum(col, axis=self._axis)
        
        self._col_dict = col_dict
        self._sensor = sensor
    
    def populate_df(self, raw_data) -> pd.DataFrame:
        """
        INPUTS  
            raw_data -> a csv file with data columns (same as self.sensors)
        """
        for sensor in self.sensors:
            # get keys 
            col = raw_data[sensor]
            self.get_statistics(col)
            keys = [sensor + "_" + k for k in self._col_dict.keys()]
            
            for key in keys:
                self._df[key] = self._col_dict.values() 
        

 