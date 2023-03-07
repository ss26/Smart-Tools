import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import os
import time
from process_data import Preprocess
import warnings
import tensorflow as tf
import OLED

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


warnings.filterwarnings('ignore')

preprocess = Preprocess()

activities = {0: 'Engrave', 1: 'Cut', 2: 'Sand', 3: 'Route'}

tflite_model = ROOT_DIR + '/models/model_11sensors_f32.tflite'

interpreter = tf.lite.Interpreter(tflite_model)
interpreter.allocate_tensors()

output_intp = interpreter.get_output_details()[0]
input_intp = interpreter.get_input_details()[0]

num_sensors = 11
num_features = 10

try:
    while True:
        tensor = preprocess.get_tensor()
        print(tensor)
        tensor = tf.cast(tensor, tf.float32)
        tensor = tf.reshape(tensor, (1, num_sensors, num_features))
        interpreter.set_tensor(input_intp['index'], tensor)
        interpreter.invoke()
        y_pred = np.argmax(interpreter.get_tensor(
            output_intp['index']), axis=1)

        print(f"Predicted Activity: {activities[y_pred[0]]}")
        OLED.print_on_OLED({activities[y_pred[0]]})
        time.sleep(1)
        
except KeyboardInterrupt:
    pass
