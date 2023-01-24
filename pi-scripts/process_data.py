"""
    Get sensor data from IMU, current sensor, microphone.
    Perform Pre-processing.
    Obtain a single pre-processed tensor.
"""
import pandas as pd
import numpy as np
import scipy as sp
import get_IMU_current
import time
import tensorflow as tf


try:
    data_getter = get_IMU_current.Current_IMU()
except RuntimeError as e:
    print("Could not start IMU")


class Preprocess:
    """
    Get live raw data, calculate statistics, output one tensor to send for inference
    """

    def __init__(self):
        self._raw_df = None
        self._processed_df = pd.DataFrame()
        self._axis = 0
        self.sensors = ["accX", "accY", "accZ", "wx",
                        "wy", "wz", "bx", "by", "bz"]
#         "Isens", "Srms"]
#         , "Isens"]  # add SRMS later
        self._col_dict = {sensor: [] for sensor in self.sensors}
        self._num_features = 10
        self._num_sensors = len(self.sensors)
        self._num_entries = 100
        self._tensor = None
        
        self._current_entry = 0
        
        for entry in range(self._num_entries):
            self.get_raw_df()
            self.calculate_stats(self._raw_df)
            self._current_entry += 1

    def get_raw_df(self):
        """
        CREATES
            One pandas DataFrame containing buffer_time worth raw data
        """

        # collect 3 seconds of raw data for one tensor
        buffer_time = time.perf_counter() + 2
        while time.perf_counter() <= buffer_time:
#             accX, accY, accZ, wx, wy, wz, bx, by, bz, Isens = data_getter.get_data()
            accX, accY, accZ, wx, wy, wz, bx, by, bz = data_getter.get_data()
            isens = np.random.rand(1,)
            srms = np.random.rand(1,)
            col_dict = {'accX': accX, 'accY': accY, 'accZ': accZ, 'wx': wx,
                        'wy': wy, 'wz': wz, 'bx': bx, 'by': by, 'bz': bz,
                        'Isens': isens, 'Srms': srms}
#             , 'Isens': Isens}
            for sensor in self.sensors:
                self._col_dict[sensor].append(col_dict[sensor])

        self._raw_df = pd.DataFrame.from_dict(self._col_dict)
        self._raw_df.dropna()

    def calculate_stats(self, raw_df: pd.DataFrame):
        """
        RETURNS
            One pandas dataframe row containing the following statistics:
            - min, max, mean, kurtosis, sem, std, variance, skew, mad, sum
        """

        assert raw_df.size != 0, f"Invalid size for dataframe: {raw_df.size}"
        assert len(raw_df.columns) == 9, f"Some sensors are missing! Number of sensors detected: {raw_df.columns}. Needed {self._num_sensors}!"
        
        # print(raw_df.describe())
        stat_df = raw_df.agg(
            ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', 'mad', 'sum'])
#         stat_df.transpose()
        stat_df = stat_df.transpose()
        
        return stat_df
    
    
    def create_processed_df(self, stat_df, processed_df):
        columns = ['accX_min', 'accX_max', 'accX_mean', 'accX_kurt', 'accX_sem', 'accX_std', 'accX_var', 'accX_skew', 'accX_mad', 'accX_sum',
                  'accY_min', 'accY_max', 'accY_mean', 'accY_kurt', 'accY_sem', 'accY_std', 'accY_var', 'accY_skew', 'accY_mad', 'accY_sum',
                  'accZ_min', 'accZ_max', 'accZ_mean', 'accZ_kurt', 'accZ_sem', 'accZ_std', 'accZ_var', 'accZ_skew', 'accZ_mad', 'accZ_sum',
                  'wx_min', 'wx_max', 'wx_mean', 'wx_kurt', 'wx_sem', 'wx_std', 'wx_var', 'wx_skew', 'wx_mad', 'wx_sum',
                  'wy_min', 'wy_max', 'wy_mean', 'wy_kurt', 'wy_sem', 'wy_std', 'wy_var', 'wy_skew', 'wy_mad', 'wy_sum',
                  'wz_min', 'wz_max', 'wz_mean', 'wz_kurt', 'wz_sem', 'wz_std', 'wz_var', 'wz_skew', 'wz_mad', 'wz_sum',
                  'bx_min', 'bx_max', 'bx_mean', 'bx_kurt', 'bx_sem', 'bx_std', 'bx_var', 'bx_skew', 'bx_mad', 'bx_sum',
                  'by_min', 'by_max', 'by_mean', 'by_kurt', 'by_sem', 'by_std', 'by_var', 'by_skew', 'by_mad', 'by_sum',
                  'bz_min', 'bz_max', 'bz_mean', 'bz_kurt', 'bz_sem', 'bz_std', 'bz_var', 'bz_skew', 'bz_mad', 'bz_sum']
#                   'Isens_min', 'Isens_max', 'Isens_mean', 'Isens_kurt', 'Isens_sem', 'Isens_std', 'Isens_var', 'Isens_skew', 'Isens_mad', 'Isens_sum',
#                   'Srms_min', 'Srms_max', 'Srms_mean', 'Srms_kurt', 'Srms_sem', 'Srms_std', 'Srms_var', 'Srms_skew', 'Srms_mad', 'Srms_sum']
        # TODO: add this after getting mic data
        
        for col in columns:
            self._processed_df[col] = [0]
        
        for col in columns:
            self._processed_df[col].values[:] = 0
        
        new_idx = pd.RangeIndex(len(self._processed_df)*10)
        self._processed_df = pd.DataFrame(np.nan, index=new_idx, columns=self._processed_df.columns)
        
        
        start_col = 0
        stop_col = start_col + self._num_features
        for sensor in self.sensors:
            values = stat_df.loc[sensor]
            values = values.to_frame().transpose()
            print(values)
            self._processed_df.iloc[self._current_entry, start_col:stop_col] = values
            start_col += self._num_features
            stop_col += self._num_features
        
        self._processed_df = self._processed_df.dropna()
        self._processed_df.to_csv('processed_df.csv', index=False)
        print(self._processed_df)

    def get_tensor(self):
        """
        RETURNS
            A single tensor to perform inference.
        """
        return tf.convert_to_tensor(self._processed_df)