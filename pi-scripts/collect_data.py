import time
import os
import pandas as pd
from process_data import Preprocess

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = ROOT_DIR + '/data/'

preprocess = Preprocess()


data_filename = input('Enter filename to store data:')

data_filename = data_filename + '.csv'

# get once to concat next
df = preprocess.get_raw_df(time.time())

try:
    while True:
        df = preprocess.get_raw_df(time.time())
        df = pd.concat([df, df], axis=1, ignore_index=True)

except KeyboardInterrupt:
    pass

df.to_csv(data_filename)