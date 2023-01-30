import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import time
from process_data import Preprocess
import warnings
import tensorflow as tf

warnings.filterwarnings('ignore')

preprocess = Preprocess()

activities = {0: 'Engrave', 1: 'Cut', 2: 'Sand', 3: 'Route'}

tflite_model = 'model.tflite'

interpreter = tf.lite.Interpreter(tflite_model)
interpreter.allocate_tensors()

output_intp = interpreter.get_output_details()[0]
input_intp = interpreter.get_input_details()[0]

try:
    while True:
        tensor = preprocess.get_tensor()
        tensor = tf.cast(tensor, tf.float32)
        tensor = tf.reshape(tensor, (1, 11, 10))
        interpreter.set_tensor(input_intp['index'], tensor)
        interpreter.invoke()
        y_pred = np.argmax(interpreter.get_tensor(
            output_intp['index']), axis=1)

        print(f"Predicted Activity: {activities[y_pred]}")
except KeyboardInterrupt:
    pass
