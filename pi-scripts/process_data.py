"""
    Get sensor data from IMU, current sensor, microphone.
    Perform Pre-processing.
    Obtain a single pre-processed tensor.
"""
import pandas as pd
import get_data
import time


try:
    data_getter = get_data.DataCollector()
except RuntimeError as e:
    print("Could not start IMU")
    exit()


class Preprocess:
    """
    Get live raw data, calculate statistics, output one tensor to send for inference
    """

    def __init__(self):
        self.sensors = ['heading', 'roll', 'pitch', 'accX', 'accY', 'accZ', 'wx', 'wy',
                        'wz', 'bx', 'by', 'bz', 'Isens', 'Srms']
        self.stats = ['min', 'max', 'mean', 'kurt', 'sem',
                      'std', 'var', 'skew', 'mad', 'sum']
        self._col_dict = {sensor: None for sensor in self.sensors}
        self._raw_df = pd.DataFrame([0]*len(self.sensors)).transpose()
        self._raw_df.columns = self.sensors

        self._processed_df = pd.DataFrame()
        self._num_features = len(self.stats)
        self._num_sensors = len(self.sensors)
        self._tensor = None
        self._raw_buffer_time = int(input("How long do you want to run the buffer, in seconds? "))
        if not isinstance(self._raw_buffer_time, int) and self._raw_buffer_time > 0:
            self._raw_buffer_time = 5       # time of serial buffer data
        
        # self._processed_buffer_time = 1     # time for processed data
        # processed_buffer_time = time.perf_counter() + self._processed_buffer_time
        # while time.perf_counter() <= processed_buffer_time:
        # print("Done one round of processing!")

    # @staticmethod
    # def get_statistics(sensor_dict):
    #     stat_dict = defaultdict(float)
    #     sensors = [k for k in sensor_dict.keys()]
    #     stats = ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', 'mad', 'sum']
    #     complete_stats = product(sensors, stats)

    def make_raw_df(self, timestamp=False):
        """
        CREATES
            One pandas DataFrame containing buffer_time worth raw data
        """

        start_time = time.perf_counter()
        print("Starting buffer...")
        while time.perf_counter() <= start_time + self._raw_buffer_time:
            heading, roll, pitch, accX, accY, accZ, wx, wy, wz, bx, by, bz, isens, mic = data_getter.get_data()

            col_dict = {
                'heading': heading, 'roll': roll, 'pitch': pitch, 'accX': accX, 
                'accY': accY, 'accZ': accZ, 'wx': wx, 'wy': wy, 'wz': wz, 'bx': bx, 
                'by': by, 'bz': bz, 'Isens': isens, 'Srms': mic
            }

            self._raw_df = pd.concat([self._raw_df, pd.DataFrame(
                [col_dict.values()], columns=self.sensors)], axis=0, ignore_index=True)

        end_time = time.perf_counter()
        print(f"Total elapsed buffer time: {end_time - start_time}")
        self._raw_df = self._raw_df.tail(-1)    # remove dummy first row
        self._raw_df.dropna()
        print(self._raw_df.columns)
        print(self._raw_df.shape)
        if timestamp:
            if 'timestamp' not in self._raw_df.columns:
                self._raw_df.insert(0, 'timestamp', time.time())
            self._raw_df['timestamp'] = time.time()

    @staticmethod
    def mad(df: pd.DataFrame):
        return (df - df.mean()).abs().mean()

    def make_processed_df(self):
        """
        CREATES
            One pandas dataframe row containing the following statistics across self.sensors:
            - min, max, mean, kurtosis, sem, std, variance, skew, mad, sum
        """

        assert self._raw_df.size != 0, f"Invalid size for dataframe: {self._raw_df.size}"
        assert len(
            self._raw_df.columns) == self._num_sensors, f"Some sensors are missing! Number of sensors detected: {len(self._raw_df.columns)}. Needed {self._num_sensors}!"

        # print(raw_df.describe())
        stat_df = self._raw_df.agg(
            ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', Preprocess.mad, 'sum'])
#         stat_df.transpose()
        stat_df = stat_df.transpose()

        self._processed_df = stat_df.unstack().to_frame().T
        self._processed_df.columns = self._processed_df.columns.map('_'.join)

    def get_raw_df(self):
        self.make_raw_df(timestamp=True)
        return self._raw_df

    def get_processed_df(self):
        return self._processed_df

    def get_tensor(self):
        # no timestamp for inference
        self.make_raw_df()
        self.make_processed_df()
        tensor_np = self._processed_df.to_numpy()
        return tensor_np
