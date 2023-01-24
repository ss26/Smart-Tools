import numpy as np
import tensorflow as tf
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import time

def plot_cf(y_true, y_pred, title_suffix):
  cm = confusion_matrix(y_true, y_pred)
  ax = sns.heatmap(cm, annot=True, fmt='g')
  ax.set_title('Confusion Matrix' + title_suffix)
  ax.set_xlabel('Predicted Activity')
  ax.set_ylabel('True Activity')
  ax.legend([])
  plt.show()
  
def accuracy(y_true, y_pred):
  cm = confusion_matrix(y_true, y_pred)
  cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
  return cm.diagonal()
  
x = np.load('test_data_x_np.npy')
y_true = np.load('test_data_y_np.npy')

# Model Inference
tflite_model = 'model.tflite'

interpreter = tf.lite.Interpreter(tflite_model)
interpreter.allocate_tensors()

output_intp = interpreter.get_output_details()[0]
input_intp = interpreter.get_input_details()[0]

y_pred_f32 = np.empty((3240,))
start_time = time.perf_counter()

for i in range(len(x)):
  tensor = x[i]
  tensor = tf.cast(tensor, tf.float32)
  tensor = tf.reshape(tensor, (1,11,10))
  interpreter.set_tensor(input_intp['index'], tensor)
  interpreter.invoke()
  y_pred_f32[i] = np.argmax(interpreter.get_tensor(output_intp['index']), axis=1)

end_time = time.perf_counter()
print(f"Quantized Model Time: {(end_time-start_time)*1000}ms")

# plot_cf(y_true, y_pred_f32, ' -- Rasberry Pi')
# print(f"Accuracy of Float64 Model: {accuracy(y_true, y_pred_f32)}")

# Quantized Model Inference (Float 32)
tflite_model_quantized = 'model_quantized_f32.tflite'

interpreter = tf.lite.Interpreter(tflite_model_quantized)
interpreter.allocate_tensors()

output_intp = interpreter.get_output_details()[0]
input_intp = interpreter.get_input_details()[0]

y_pred_f32q = np.empty((3240,))
start_time = time.perf_counter()
for i in range(len(x)):
  tensor = x[i]
  tensor = tf.cast(tensor, tf.float32)
  tensor = tf.reshape(tensor, (1,11,10))
  interpreter.set_tensor(input_intp['index'], tensor)
  interpreter.invoke()
  y_pred_f32q[i] = np.argmax(interpreter.get_tensor(output_intp['index']), axis=1)

end_time = time.perf_counter()
print(f"Quantized Model Time: {(end_time-start_time)*1000}ms")

# plot_cf(y_true, y_pred_f32q, ' -- Rasberry Pi, Quantized (Float32)')
# print(f"Accuracy of Float32 Quantized Model: {accuracy(y_true, y_pred_f32q)}")

# Quantized Model Inference (Int 8)
# tflite_model_quantized = 'model_quantized_int8.tflite'
# 
# interpreter = tf.lite.Interpreter(tflite_model_quantized)
# interpreter.allocate_tensors()
# 
# output_intp = interpreter.get_output_details()[0]
# input_intp = interpreter.get_input_details()[0]
# 
# y_pred_int8q = np.empty((3240,))
# for i in range(len(x)):
#   tensor = x[i]
#   tensor = tf.cast(tensor, tf.int8)
#   tensor = tf.reshape(tensor, (1,11,10))
#   interpreter.set_tensor(input_intp['index'], tensor)
#   interpreter.invoke()
#   y_pred_int8q[i] = np.argmax(interpreter.get_tensor(output_intp['index']), axis=1)
# 
# plot_cf(y_true, y_pred_int8q, ' -- Rasberry Pi, Quantized (Int 8)')
# print(f"Accuracy of Int8 Quantized Model: {accuracy(y_true, y_pred_int8q)}")