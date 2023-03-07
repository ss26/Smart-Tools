import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import os
import time
from process_data import Preprocess
from statistics import mode
import warnings
import tensorflow as tf
import OLED

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


warnings.filterwarnings('ignore')

preprocess = Preprocess()

activities = {0: 'Engrave', 1: 'Cut', 2: 'Sand', 3: 'Route'}

tflite_model = ROOT_DIR + '/models/model-pi10mins.tflite'

interpreter = tf.lite.Interpreter(tflite_model)
interpreter.allocate_tensors()

output_intp = interpreter.get_output_details()[0]
input_intp = interpreter.get_input_details()[0]

num_sensors = 11
num_features = 10

try:
    processed_df = preprocess.get_processed_df(raw_buf_time=30)
    raw_df = preprocess.get_raw_df()
    raw_df.to_csv(ROOT_DIR + "/data/test-raw-df.csv", header=raw_df.columns)
    y_preds = []
    for i in range(len(processed_df)):
        tensor = preprocess.get_custom_tensor(processed_df.iloc[i,:])
        tensor = tf.cast(tensor, tf.float32)
        tensor = tf.reshape(tensor, (1, num_sensors, num_features))
        interpreter.set_tensor(input_intp['index'], tensor)
        interpreter.invoke()
        y_pred = np.argmax(interpreter.get_tensor(
            output_intp['index']), axis=1)
        print(f"y_pred: {y_pred[0]}")
        y_preds += [y_pred[0]]

    y_pred_mode = mode(y_preds)
    print(f"Predicted Activity: {activities[y_pred_mode]}")
    OLED.print_on_OLED({activities[y_pred_mode]})
    time.sleep(1)
        
except KeyboardInterrupt:
    pass
