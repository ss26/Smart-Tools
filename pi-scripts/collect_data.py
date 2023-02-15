import time
import os
import pandas
from process_data import Preprocess

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = ROOT_DIR + '/data/'

preprocess = Preprocess()

data_filename = str(time.time()) + '.csv'

df = preprocess.get_processed_df()

df.to_csv(data_filename)