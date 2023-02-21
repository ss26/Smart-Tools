import pandas as pd
from tqdm import tqdm 
import warnings

warnings.filterwarnings('ignore')


num_sensors = 11

def make_processed_df(raw_df, activity):
    """Copy pasted from process_data for ease of use."""

    def mad(df: pd.DataFrame):
        return (df - df.mean()).abs().mean()

    raw_df = raw_df.filter(['accX','accY','accZ','wx','wy','wz','bx','by','bz','Isens','Srms'], axis=1)
    assert raw_df.size != 0, f"Invalid size for dataframe: {raw_df.size}"
    assert len(
        raw_df.columns) == num_sensors, f"Some sensors are missing! Number of sensors detected: {len(raw_df.columns)}. Needed {num_sensors}!"

    processed_df = pd.DataFrame()

    for i in tqdm(range(1396)):
        _processed_df = pd.DataFrame()
        raw_df_buf = raw_df.iloc[i:i+3,:]
        stat_df = raw_df_buf.agg(
            ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', mad, 'sum'], bias=False)        
        _processed_df = stat_df.unstack().to_frame().T
        _processed_df.columns = _processed_df.columns.map('_'.join)
        processed_df = processed_df.append(_processed_df)
    processed_df['Activity'] = activity
    return processed_df


data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_routing.csv'

df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/reshaped_routing.csv')
proc_df = make_processed_df(df, 3)

proc_df.to_csv(data_filename)