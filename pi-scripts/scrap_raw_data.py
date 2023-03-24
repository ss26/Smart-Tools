import os
import pandas as pd
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def make_processed_df(raw_df, activity=None):
    """Copy pasted from process_data for ease of use."""
    num_sensors = 11

    def mad(df: pd.DataFrame):
        return (df - df.mean()).abs().mean()

    raw_df = raw_df.filter(['accX', 'accY', 'accZ', 'wx',
                           'wy', 'wz', 'bx', 'by', 'bz', 'Isens', 'Srms'], axis=1)
    assert raw_df.size != 0, f"Invalid size for dataframe: {raw_df.size}"
    assert len(
        raw_df.columns) == num_sensors, f"Some sensors are missing! Number of sensors detected: {len(raw_df.columns)}. Needed {num_sensors}!"

    if raw_df.shape[0] % 590 != 0:
        raw_df = raw_df.tail((raw_df.shape[0] - raw_df.shape[0] % 590))

    processed_df = pd.DataFrame()

    # ar
    for i in tqdm(range(0, 13520, 520)):
        _processed_df = pd.DataFrame()
        raw_df_buf = raw_df.iloc[i:i+1040, :]
        stat_df = raw_df_buf.agg(
            ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', mad, 'sum'])
        _processed_df = stat_df.unstack().to_frame().T
        _processed_df.columns = _processed_df.columns.map('_'.join)
        processed_df = processed_df.append(_processed_df)
    processed_df['Activity'] = activity

    return processed_df


def main():
    raw_data_folders = ['Run_1_Samples', 'Run_2_Samples', 'Run_3_Samples', 'Run_4_Samples', 'Run_5_Samples',
                        'Run_6_Samples', 'Run_7_Samples', 'Run_8_Samples', 'Run_9_Samples', 'RGL_data']

    paths_list = []

    csv_format = '.csv'
    data_folder_root = ROOT_DIR + '/data/raw_data/'

    for folder in raw_data_folders:
        for _, _, files in os.walk(data_folder_root + folder):
            paths_list += [filename for filename in files if filename[-4:] == csv_format]

    paths_list = list(set(paths_list))
    
    print(len(paths_list))

if __name__ == '__main__':
    main()
