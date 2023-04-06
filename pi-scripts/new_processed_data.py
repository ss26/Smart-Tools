import pandas as pd
from tqdm import tqdm
import warnings
import os

warnings.filterwarnings('ignore')


num_sensors = 11


def make_processed_df(folder, raw_df_path, activity=None):
    """Copy pasted from process_data for ease of use."""

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

    raw_df_len = raw_df.shape[0]
    
    processed_df = pd.DataFrame()

    activities = {'E': 0, 'C': 1, 'S': 2, 'R': 3}

    # ar
    for i in tqdm(range(0, raw_df_len, 520)):
        _processed_df = pd.DataFrame()
        raw_df_buf = raw_df.iloc[i:i+1040, :]
        stat_df = raw_df_buf.agg(
            ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', mad, 'sum'])
        _processed_df = stat_df.unstack().to_frame().T
        _processed_df.columns = _processed_df.columns.map('_'.join)
        processed_df = processed_df.append(_processed_df)

    try:
        processed_df['Activity'] = activities[raw_df_path[2]]
    except KeyError:
        print(raw_df_path[2])

    return processed_df

    # r-pi
    # for i in tqdm(range(0,raw_df.shape[0],295)):
    #     _processed_df = pd.DataFrame()
    #     raw_df_buf = raw_df.iloc[i:i+590,:]
    #     stat_df = raw_df_buf.agg(
    #         ['min', 'max', 'mean', 'kurt', 'sem', 'std', 'var', 'skew', mad, 'sum'])
    #     _processed_df = stat_df.unstack().to_frame().T
    #     _processed_df.columns = _processed_df.columns.map('_'.join)
    #     processed_df = processed_df.append(_processed_df)
    # if activity:
    #     processed_df['Activity'] = activity
    # return processed_df

# for arduino
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_ar_engraving.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_ar_cutting.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_ar_sanding.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_ar_routing.csv'

# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_ar_engraving.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_ar_cutting.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_ar_sanding.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_ar_routing.csv')

# proc_df = make_processed_df(df, 0)
# proc_df = make_processed_df(df, 1)
# proc_df = make_processed_df(df, 2)
# proc_df = make_processed_df(df, 3)

# for pi
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_engraving.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_cutting.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_sanding.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_routing.csv'

# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_engraving.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_cutting.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_sanding.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_routing.csv')

# proc_df = make_processed_df(df, 0)
# proc_df = make_processed_df(df, 1)
# proc_df = make_processed_df(df, 2)
# proc_df = make_processed_df(df, 3)

# for pi conv
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_conv_engraving.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_conv_cutting.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_conv_sanding.csv'
# data_filename = '/home/ss26/Projects/Smart-Tools/data/processed_pi_conv_routing.csv'

# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_conv_engraving.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_conv_cutting.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_conv_sanding.csv')
# df = pd.read_csv('/home/ss26/Projects/Smart-Tools/data/compare_pi_conv_routing.csv')

# proc_df = make_processed_df(df, 0)
# proc_df = make_processed_df(df, 1)
# proc_df = make_processed_df(df, 2)
# proc_df = make_processed_df(df, 3)

# custom dfs


data_folder = '/home/ss26/Projects/Smart-Tools/data/Arduino_Yaskawa'
processed_filename = '/home/ss26/Projects/Smart-Tools/data/S2023_Yaskawa_Processed.csv'

data_filenames = []
csv_format = '.csv'

for root, dirs, files in os.walk(data_folder):
    data_filenames += [filename for filename in files if filename[-4:] == csv_format]

data_filenames = list(set(data_filenames))

print(data_filenames)

processed_df = pd.DataFrame()

for filename in data_filenames:
    proc_df = make_processed_df(data_folder, filename)
    processed_df = pd.concat([processed_df, proc_df], ignore_index=True)

processed_df.to_csv(processed_filename)
