"""
    Get sensor data from IMU, current sensor, microphone.
    Perform Pre-processing.
    Obtain a single pre-processed tensor.
"""
import pandas as pd
import get_IMU_current
import time


try:
    data_getter = get_IMU_current.Current_IMU()
except RuntimeError as e:
    print("Could not start IMU")


class Preprocess:
    """
    Get live raw data, calculate statistics, output one tensor to send for inference
    """

    def __init__(self):
        self.sensors = ['accX', 'accY', 'accZ', 'wx', 'wy',
                        'wz', 'bx', 'by', 'bz']
        #         "Isens", "Srms"]
        self.stats = ['min', 'max', 'mean', 'kurt', 'sem',
                      'std', 'var', 'skew', 'mad', 'sum']
        self._col_dict = {sensor: None for sensor in self.sensors}
        self._raw_df = pd.DataFrame([0]*len(self.sensors)).transpose()

        self._processed_df = pd.DataFrame()
        self._num_features = len(self.stats)
        self._num_sensors = len(self.sensors)
        self._tensor = None
        self._raw_buffer_time = 0.01        # time of serial buffer data
        # self._processed_buffer_time = 1     # time for processed data

        # processed_buffer_time = time.perf_counter() + self._processed_buffer_time
        # while time.perf_counter() <= processed_buffer_time:
        self.get_raw_df()
        self.get_processed_df()
        # print("Done one round of processing!")

    # @staticmethod
    # def get_statistics(sensor_dict):
    #     stat_dict = defaultdict(float)
    #     sensors = [k for k in sensor_dict.keys()]
    #     stats = ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', 'mad', 'sum']
    #     complete_stats = product(sensors, stats)

    def get_raw_df(self):
        """
        CREATES
            One pandas DataFrame containing buffer_time worth raw data
        """

        # collect 3 seconds of raw data for one tensor
        buffer_time = time.perf_counter() + self._raw_buffer_time
        while time.perf_counter() <= buffer_time:
            accX, accY, accZ, wx, wy, wz, bx, by, bz = data_getter.get_data()

            col_dict = {
                'accX': accX, 'accY': accY, 'accZ': accZ, 'wx': wx,
                'wy': wy, 'wz': wz, 'bx': bx, 'by': by, 'bz': bz
            }

            # add these two after attaching current sensor and mic
            # isens = np.random.rand(1,)
            # srms = np.random.rand(1,)

            self._raw_df = pd.concat([self._raw_df, pd.DataFrame(
                [col_dict.values()], columns=self.sensors)], axis=0, ignore_index=True)

        self._raw_df.dropna()

    @staticmethod
    def mad(df: pd.DataFrame):
        return (df - df.mean()).abs().mean()

    def get_processed_df(self):
        """
        CREATES
            One pandas dataframe row containing the following statistics across self.sensors:
            - min, max, mean, kurtosis, sem, std, variance, skew, mad, sum
        """

        assert self.raw_df.size != 0, f"Invalid size for dataframe: {self.raw_df.size}"
        assert len(
            self.raw_df.columns) == self._num_sensors, f"Some sensors are missing! Number of sensors detected: {self.raw_df.columns}. Needed {self._num_sensors}!"

        # print(raw_df.describe())
        stat_df = self.raw_df.agg(
            ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', Preprocess.mad, 'sum'])
#         stat_df.transpose()
        stat_df = stat_df.transpose()

        self._processed_df = stat_df.unstack().to_frame().T
        self._processed_df.columns = self._processed_df.columns.map('_'.join)

    def get_tensor(self):
        return self._processed_df.to_numpy()
