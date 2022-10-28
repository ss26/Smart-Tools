"""
    Get sensor data from IMU, current sensor, microphone.
    Perform Pre-processing.
    Obtain a single pre-processed tensor.
"""
import pandas as pd
import numpy as np
import scipy
import imu_file  # IMU sensor script
import current_file  # Current sensor script


def get_IMU():
    imu_data = imu_file.get_data()
    return imu_data


def get_current():
    current_data = current_file.get_data()
    return current_data

class Preprocess:
    def __init__():
        df = pd.DataFrame()
    
    def get_statistics(self, col: np.array) -> dict:
        """
        Statistics used:
            - min, max
            - mean, kurtosis, sem
            - std, variance, skew
            - mad, sum
        """
        assert col.size != 0, f"Invalid size for data column: {col.size}"
        col_dict = dict()
        col_dict["max"] = np.amax(col)
        col_dict["min"] = np.amin(col)
        col_dict["mean"] = np.mean(col)
        col_dict["kurtosis"] = scipy.stats.kurtosis(col)
        col_dict["skew"] = scipy.stats.kurtosis(col)
        col_dict["std"] = np.std(col)
        
