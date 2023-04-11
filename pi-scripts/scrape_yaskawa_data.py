import os
import pandas as pd
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def make_processed_df(folder, raw_df_path, activity=None):
    """Copy pasted from process_data for ease of use."""
    num_sensors = 11

    raw_df = pd.read_csv(folder + '/' + raw_df_path)

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
        processed_df['Activity'] = activities[raw_df_path[2]]
    except KeyError:
        print(raw_df_path[2])

    return processed_df


def main():
    data_folder_root = ROOT_DIR + '/data/Arduino_Yaskawa/'

    paths_list = []

    csv_format = '.csv'

    for _, _, files in os.walk(data_folder_root):
        paths_list += [filename for filename in files if filename[-4:] == csv_format]

    paths_list = list(set(paths_list)) 

    mega_processed_df = pd.DataFrame()

    for path in tqdm(paths_list):
        processed_df = make_processed_df(data_folder_root, path)
        mega_processed_df = pd.concat([mega_processed_df, processed_df], ignore_index=True)
    
    print(mega_processed_df.shape)
    processed_filename = '/home/ss26/Projects/Smart-Tools/data/S2023_Yaskawa_Smoothened.parquet'

    if os.path.exists(processed_filename):
        print("Older version of dataframe exists. Deleting and overwriting...")
        os.remove(processed_filename)
    
    mega_processed_df.to_parquet(processed_filename)

    if os.path.exists(processed_filename):
        print("Successfully created processed dataframe of Spring 2023 Yaskawa data!")
    else:
        print("Processed dataframe was not saved to parquet, check code!")

if __name__ == '__main__':
    main()
