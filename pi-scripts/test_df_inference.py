import time
import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import tensorflow as tf

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def get_y_test_df():
    test_df = pd.read_csv(ROOT_DIR + '/data/OL50_10secframe_Proccessed_Test_Xy_Matrix.csv')
    y = test_df['Activity']
    
    # remove_isens = ['Isens_min', 'Isens_max', 'Isens_mean', 'Isens_kurt', 'Isens_sem',
    #             'Isens_std', 'Isens_var', 'Isens_skew', 'Isens_mad', 'Isens_sum']

    # remove_srms = ['Srms_min', 'Srms_max', 'Srms_mean', 'Srms_kurt', 'Srms_sem',
    #           'Srms_std', 'Srms_var', 'Srms_skew', 'Srms_mad', 'Srms_sum']              
    remove_unnamed = ['Unnamed: 0', 'Subject Number', 'Trial']

    test_df = test_df.drop(remove_unnamed, axis=1)
    return y, test_df

def plot_cf(y_true, y_pred, title_suffix, save=False):
    cm = confusion_matrix(y_true, y_pred)
    ax = sns.heatmap(cm, annot=True, fmt='g')
    ax.set_title('Confusion Matrix' + title_suffix)
    ax.set_xlabel('Predicted Activity')
    ax.set_ylabel('True Activity')
    ax.legend([])
    plt.show()
    if save is True:
        plt.savefig('cm.png')

def accuracy(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
    return cm.diagonal()

# model = tf.keras.models.load_model('/home/ss26/Projects/Smart-Tools/pi-scripts/9sensors_model')
tflite_model = ROOT_DIR + '/models/model.tflite'

num_sensors = 11
num_features = 10

interpreter = tf.lite.Interpreter(tflite_model)
interpreter.allocate_tensors()

output_intp = interpreter.get_output_details()[0]
input_intp = interpreter.get_input_details()[0]

y_true, test_df = get_y_test_df()
# y_true = test_df['Activity']
y_pred_f32 = np.zeros(len(test_df))
# x = get_x()
# y_pred_f32 = np.argmax(model.predict(x), axis=1)
start_time = time.perf_counter()

x = np.load(ROOT_DIR + '/data/test_data_x_np.npy')

for i, value in enumerate(x):
  tensor = value
  tensor = tf.cast(tensor, tf.float32)
  tensor = tf.reshape(tensor, (1,num_sensors,num_features))
  interpreter.set_tensor(input_intp['index'], tensor)
  interpreter.invoke()
  y_pred_f32[i] = np.argmax(interpreter.get_tensor(output_intp['index']), axis=1)

end_time = time.perf_counter()
print(f"Model Inference Time for N={len(test_df)} inferences: {(end_time-start_time)*1000}ms")

plot_cf(y_true, y_pred_f32, ' -- Raspberry Pi', save=False)
print(f"Accuracy of Float32 Model: {accuracy(y_true, y_pred_f32)}")