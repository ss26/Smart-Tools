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
        self.timestamp = ['timestamp']
        # add roll, pitch, yaw when needed to self.sensors
        self.sensors = ['accX', 'accY', 'accZ', 'wx', 'wy',
                        'wz', 'bx', 'by', 'bz', 'Isens', 'Srms']
        self.stats = ['min', 'max', 'mean', 'kurt', 'sem',
                      'std', 'var', 'skew', 'mad', 'sum']
        self._col_dict = {sensor: None for sensor in self.sensors}

        self._raw_df = pd.DataFrame(
            [0]*len(self.timestamp + self.sensors)).transpose()
        self._raw_df.columns = self.timestamp + self.sensors
        self._activities = {0: 'Engrave', 1: 'Cut', 2: 'Sand', 3: 'Route'}

        self._processed_df = pd.DataFrame()
        self._num_features = len(self.stats)
        self._num_sensors = len(self.sensors)
        self._tensor = None
        
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

    def make_raw_df(self, timestamp=False, labels=False, raw_buf_time=None):
        """
        CREATES
            One pandas DataFrame containing buffer_time worth raw data
        """
        if isinstance(raw_buf_time, int):
            self._raw_buffer_time = raw_buf_time       # time of serial buffer data
        else:
            self._raw_buffer_time = int(
                input("How long do you want to run the buffer, in seconds? "))
                    
        if labels:
            activity = input("What activity are you doing? ")
            activity = list(self._activities.values()).index(activity)
            self._raw_df = pd.DataFrame(
                [0]*(len(self.sensors) + 2))  # timestamp and activity
            # self._raw_df.columns = self.timestamp + self.sensors

        print("Starting buffer...")

        start_time = time.perf_counter()

        while time.perf_counter() <= start_time + self._raw_buffer_time:
            heading, roll, pitch, accX, accY, accZ, wx, wy, wz, bx, by, bz, isens, mic = data_getter.get_data()
            if timestamp:
                col_dict = {
                    'timestamp': time.perf_counter() - start_time, 'roll': roll, 'pitch': pitch, 'yaw': heading,
                    'accX': accX, 'accY': accY, 'accZ': accZ, 'wx': wx, 'wy': wy, 'wz': wz, 'bx': bx,
                    'by': by, 'bz': bz, 'Isens': isens, 'Srms': mic, 'activity': activity
                }

                self._raw_df = pd.concat([self._raw_df, pd.DataFrame(
                    [col_dict.values()], columns=self.timestamp + self.sensors + ['Activity'])], axis=0, ignore_index=True)

            else: 
                col_dict = {
                    'accX': accX, 'accY': accY, 'accZ': accZ, 'wx': wx, 'wy': wy, 'wz': wz, 'bx': bx,
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

    @staticmethod
    def mad(df: pd.DataFrame):
        return (df - df.mean()).abs().mean()

    def make_processed_df(self, raw_df):
        """
        CREATES
            One pandas dataframe row containing the following statistics across self.sensors:
            - min, max, mean, kurtosis, sem, std, variance, skew, mad, sum
        """
        # if not raw_df:
        #     raw_df = self._raw_df

        assert raw_df != 0, f"Invalid size for dataframe: {raw_df.size}"
        assert len(
            raw_df.columns) == self._num_sensors, f"Some sensors are missing! Number of sensors detected: {len(raw_df.columns)}. Needed {self._num_sensors}!"

        if len(raw_df)%590 != 0:
            raw_df = raw_df.tail(-len(raw_df)%590)

        for i in range(0,len(raw_df), 295):
            raw_df_buf = raw_df.iloc[i:i+590,:]
            stat_df = raw_df_buf.agg(
                ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', Preprocess.mad, 'sum'])
            stat_df = stat_df.transpose()
            processed_df = stat_df.unstack().to_frame().T
            processed_df.columns = processed_df.columns.map('_'.join)
            self._processed_df.append(processed_df)
        

    def get_raw_df(self, timestamp, labels):
        self.make_raw_df(timestamp=timestamp, labels=labels)
        return self._raw_df

    def get_processed_df(self, raw_buf_time=None):
        self.make_raw_df(raw_buf_time=raw_buf_time)
        self.make_processed_df(self._raw_df)
        return self._processed_df

    def get_tensor(self,raw_buf_time=None ):
        # no timestamp for inference
        self.make_raw_df(raw_buf_time)
        self.make_processed_df(self._raw_df)
        tensor_np = self._processed_df.to_numpy()
        return tensor_np
    
    @staticmethod
    def get_custom_tensor(df: pd.DataFrame):
        return df.to_numpy()