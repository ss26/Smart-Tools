import os
import pandas as pd
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def make_processed_df(raw_df_path, activity=None):
    """Copy pasted from process_data for ease of use."""
    num_sensors = 11

    raw_df = pd.read_csv(raw_df_path)

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

    activities = {'E': 0, 'C': 1, 'S': 2, 'R': 3}
    
    # smoothen data
    window = int(0.25*104)
    raw_df = raw_df.rolling(window=window).mean().dropna().reset_index(drop=True)

    processed_df = raw_df
    # # ar
    # for i in tqdm(range(0, 13520, 520)):
    #     _processed_df = pd.DataFrame()
    #     raw_df_buf = raw_df.iloc[i:i+1040, :]
        
    #     raw
        # stat_df = raw_df_buf.agg(
        #     ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', mad, 'sum'])
        # _processed_df = stat_df.unstack().to_frame().T
        # _processed_df.columns = _processed_df.columns.map('_'.join)
        # processed_df = processed_df.append(_processed_df)
    
    try:
        processed_df['Activity'] = activities[raw_df_path[-15]]
    except KeyError:
        print(raw_df_path[-15])

    return processed_df


def main():
    raw_data_folders = ['Run_1_Samples', 'Run_2_Samples', 'Run_3_Samples', 'Run_4_Samples', 'Run_5_Samples',
                        'Run_6_Samples', 'Run_7_Samples', 'Run_8_Samples', 'Run_9_Samples', 'RGL_data']

    paths_list = []

    csv_format = '.csv'
    data_folder_root = ROOT_DIR + '/data/raw_data/'

    for folder in raw_data_folders:
        for root, _, files in os.walk(data_folder_root + folder):
            paths_list += [root + '/' + filename for filename in files if filename[-4:] == csv_format]

    paths_list = list(set(paths_list)) 
    
    mega_processed_df = pd.DataFrame()

    for path in tqdm(paths_list):
        processed_df = make_processed_df(path)
        mega_processed_df = pd.concat([mega_processed_df, processed_df], ignore_index=True)
    
    print(mega_processed_df.shape)

    mega_processed_df.to_csv('/home/ss26/Projects/Smart-Tools/data/F2021_processed.csv')

    if os.path.exists('/home/ss26/Projects/Smart-Tools/data/F2021_processed.csv'):
        print("Successfully created processed dataframe of Fall 2021 raw data!")

if __name__ == '__main__':
    main()
