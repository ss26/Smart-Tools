import pandas as pd
import os
from collections import OrderedDict
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from sklearn.metrics import log_loss
import seaborn as sns
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import shutil
import warnings
import random

warnings.filterwarnings('ignore')


def get_activity_df(df, percent):
    df0 = df.loc[df['Activity'] == 0]
    df1 = df.loc[df['Activity'] == 1]
    df2 = df.loc[df['Activity'] == 2]
    df3 = df.loc[df['Activity'] == 3]

    def data_num(x): return int(percent*x)

    df_combined = pd.concat([
        df0[:data_num(df0.shape[0])],
        df1[:data_num(df1.shape[0])],
        df2[:data_num(df2.shape[0])],
        df3[:data_num(df3.shape[0])]
    ], ignore_index=True)

    return df_combined


def get_xy_numpy(df, x_features_columns, y_features_columns='Activity'):
    x_df = df[x_features_columns]
    x_np = x_df.to_numpy()
    # get the output column we want to predict
    y_df = df[y_features_columns]
    y_np = y_df.to_numpy()
    # assert the x and y dataframes do NOT have any null or NaN entries
    assert(x_df.isnull().sum().sum() == 0)
    assert(y_df.isnull().sum().sum() == 0)

    return x_np, y_np, x_df, y_df


def build_1D_CNN(model_base_dir, model_name='1DCNN', num_sensors=11, num_features=10, num_outputs=4):
    """Builds a convolutional neural network in Keras."""
    model = tf.keras.Sequential([
        tf.keras.layers.Dropout(rate=0.5),
        tf.keras.layers.Conv1D(45, 3, activation='relu',
                               input_shape=(num_sensors, num_features)),
        tf.keras.layers.MaxPooling1D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(784, activation='relu'),
        tf.keras.layers.Dense(num_outputs, activation='softmax')])

    model_path = None

    #model_path = os.path.join(model_base_dir + "./netmodels", "1DCNN")
    #print("Built CNN.")
    # if not os.path.exists(model_path):
    #  os.makedirs(model_path)
    #model.load_weights(model_base_dir + "./netmodels/1DCNN/weights.h5")

    return model, model_path


def calculate_model_size(model):
    print(model.summary())
    var_sizes = [
        np.product(list(map(int, v.shape))) * v.dtype.size
        for v in model.trainable_variables
    ]
    model_size = sum(var_sizes) / 1024

    print("Model size:", model_size, "KB")
    return model_size


def get_preds(test_data, test_df: pd.DataFrame, model, title):
    x = np.concatenate([x for x, y in test_data], axis=0)
    y = np.concatenate([y for x, y in test_data], axis=0)

    y_true = test_df['Activity'].to_numpy()
    confidences = model.predict(test_data)
    y_pred = np.argmax(confidences, axis=1)

    loss, acc = model.evaluate(test_data, verbose=0)

    # plot_cf(y_true, y_pred, title, save=True)
    logloss = log_loss(y_true, confidences)

    return loss, acc, logloss


def plot_cf(y_true, y_pred, title, save=False):
    cm = confusion_matrix(y_true, y_pred)
    ax = sns.heatmap(cm, annot=True, fmt='g')
    ax.set_title(title)
    ax.set_xlabel('Predicted Activity')
    ax.set_xticklabels(['Engrave', 'Cut', 'Sand', 'Route'])
    ax.set_ylabel('True Activity')
    ax.set_yticklabels(['Engrave', 'Cut', 'Sand', 'Route'])
    ax.legend([])
    if not save:
        plt.show()
        plt.cla()
    else:
        plt.savefig(
            '/home/ss26/Projects/Smart-Tools/progress/apr5/dim_returns/'+title+'.png', dpi=300)
        plt.cla()
    ax.cla()
    plt.cla()


def accuracy(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]
    return cm.diagonal()


def plot_data_vs_acc(percents, accs, title):
    plt.cla()
    plt.plot([percent*100 for percent in percents],
             [acc*100 for acc in accs], 'xg--')
    plt.title(f"Test Accuracy vs Dataset volume - " + title)
    plt.xlabel("Percentage of Data (in %)")
    plt.ylabel("Accuracy (in %)")
    # plt.savefig("/home/ss26/Projects/Smart-Tools/progress/apr5/accs_vs_data/" + title + ".png", dpi=600)


def plot_data_vs_logloss(percents, lls, title):
    plt.cla()
    plt.plot([percent*100 for percent in percents], lls, 'xm--')
    plt.title(f"Log-Loss vs Dataset volume - " + title)
    plt.xlabel("Percentage of Data (in %)")
    plt.ylabel("Log Loss")
    # plt.savefig("/home/ss26/Projects/Smart-Tools/progress/apr5/lls_vs_data/" + title + ".png", dpi=600)


def main(SEED):

    BATCH_SIZE = 64
    SHUFFLE_BUFFER_SIZE = 100

    epochs = 15

    # Yaswaka
    train_df_yaskawa = pd.read_csv(
        '/home/ss26/Projects/Smart-Tools/data/Yaskawa_Train_Xy_Matrix.csv')
    # val_df_yaskawa = pd.read_csv(
    # '/home/ss26/Projects/Smart-Tools/data/Yaskawa_Validate_Xy_Matrix.csv')
    # test_df_yaskawa = pd.read_csv(
    # '/home/ss26/Projects/Smart-Tools/data/Yaskawa_Test_Xy_Matrix.csv')

    # human
    train_df_human = pd.read_csv(
        '/home/ss26/Projects/Smart-Tools/data/Human_Train_Xy_Matrix.csv')
    val_df_human = pd.read_csv(
        '/home/ss26/Projects/Smart-Tools/data/Human_Validate_Xy_Matrix.csv')
    test_df_human = pd.read_csv(
        '/home/ss26/Projects/Smart-Tools/data/Human_Test_Xy_Matrix.csv')

    x_features_columns = [colname for colname in list(train_df_human) if colname not in [
        'Unnamed: 0', 'Activity', 'Subject Number', 'Trial', 'Unnamed: 0.1']]
    y_features_columns = 'Activity'
    data_percents_human = np.arange(0, 1, 0.02)
    data_percents_human = data_percents_human[1:]

    losses, accs, loglosses = [], [], []

    num_activities = 4

    # title = f"Human trained + no pretraining (Seed: {SEED})"
    title = f"Human trained + Yaskawa pretraining (Seed: {SEED})"

    for percent in tqdm(data_percents_human):

        train_df_human_percent = get_activity_df(train_df_human, percent)
        # train_df_yaskawa_percent = get_activity_df(train_df_yaskawa, percent*(1/4))
        # val_df_percent = get_activity_df(val_df, percent)
        # test_df_percent = get_activity_df(test_df, percent)

        train_test_val_df_dict = OrderedDict()
        train_test_val_df_dict['train'] = train_df_human_percent
        # train_test_val_df_dict['train'] = pd.concat([train_df_human_percent, train_df_yaskawa_percent], ignore_index=True)
        train_test_val_df_dict['val'] = val_df_human
        train_test_val_df_dict['test'] = test_df_human

        tf_dataset_dict = OrderedDict()

        # min, max, mean etc.
        num_features = 10
        num_sensors = int(len(x_features_columns)/num_features)

        for data_split, data_df in train_test_val_df_dict.items():

            data_x_np, data_y_np, data_x_df, data_y_df = get_xy_numpy(
                data_df, x_features_columns, y_features_columns=y_features_columns)

            quantile_list = [.001, 0.25, 0.5, 0.75, 0.999]

            # only for training data, get the above quantiles for ALL COLUMNS and save to a csv
            if data_split == 'train':
                # do not use sklearn, instead save the following quantiles of data to a dataframe and store as a csv
                train_quantile_df = data_x_df.quantile(quantile_list)
                # train_quantile_df.to_csv('/home/ss26/Projects/Smart-Tools/notebooks/outputs/yaskawa/train_normalization_quantiles.csv')

            # for all data, scale each column using the same PER-COLUMN scaling as the training data for uniformity
            normalized_data_x_df = data_x_df.copy()
            for feature_name in data_x_df.columns:

                # do not use absolute min, max due to OUTLIERS!
                min_value = train_quantile_df[feature_name][quantile_list[0]]
                max_value = train_quantile_df[feature_name][quantile_list[-1]]

                normalized_data_x_df[feature_name] = (
                    data_x_df[feature_name] - min_value) / (max_value - min_value)

        # now actually transform the training data
            data_x_np_scaled = normalized_data_x_df.to_numpy()

            # BATCH_SIZE x NUM_SENSORS x NUM_FEATURES
            # view this as an image with 1 channel, NUM_SENSORS x NUM_FEATURES size

            reshaped_data_x_np_scaled = data_x_np_scaled.reshape(
                [-1, num_sensors, num_features])

            # get a tensorflow dataset
            tf_dataset = tf.data.Dataset.from_tensor_slices(
                (reshaped_data_x_np_scaled, data_y_np))

            # load the tensorflow dataset
            tf_dataset_dict[data_split] = tf_dataset

        train_data = tf_dataset_dict['train'].shuffle(
            SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
        val_data = tf_dataset_dict['val'].batch(BATCH_SIZE)
        test_data = tf_dataset_dict['test'].batch(BATCH_SIZE)

        # find the number of batches in the TESTING dataset
        # this is useful later
        test_len = 0
        for batch in test_data:
            test_len += 1

        # 1D CNN model
        model_base_dir = "/home/ss26/Projects/Smart-Tools/notebooks/outputs/" + title + "/model"
        base_dir = "/home/ss26/Projects/Smart-Tools/notebooks/outputs/" + title

        if not os.path.isdir(model_base_dir):
            os.makedirs(model_base_dir)
        else:
            shutil.rmtree(model_base_dir)

        # model, model_path = build_1D_CNN(model_base_dir, model_name='1DCNN',
            # num_sensors=num_sensors, num_features=num_features, num_outputs=num_activities)

        model = tf.keras.models.load_model(
            '/home/ss26/Projects/Smart-Tools/models/yaskawa_pretrained_dropout')

        # when we train, we save a csv of the training accuracy/loss
        csv_logger = tf.keras.callbacks.CSVLogger(
            base_dir + '/training.log')

        # how long we train, set up model with loss function
        # do 50 for convergence, do 5 to test code
        model.compile(optimizer="adam",
                      loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])

        # now, finally start training
        model.fit(train_data,
                  epochs=epochs,
                  validation_data=val_data,
                  callbacks=[csv_logger], verbose=0)

        loss, acc, ll = get_preds(
            test_data, test_df_human, model, f'{percent*100}% of data')
        losses += [loss]
        accs += [acc]
        loglosses += [ll]

    # plot_data_vs_acc(data_percents_human, accs, title)
    # plot_data_vs_logloss(data_percents_human, loglosses, title)

    metrics = pd.DataFrame(list(zip(data_percents_human, accs, loglosses)), columns=[
        "percent", "accuracy", "logloss"])
    metrics.to_csv(
        "/home/ss26/Projects/Smart-Tools/progress/apr5/" + title + ".csv")

    print(f"Saved metrics of " + title + "!")

    print("End of experiment")


if __name__ == '__main__':

    SEEDS = [42, 43, 44, 45, 46]

    for SEED in SEEDS:
        tf.keras.utils.set_random_seed(SEED)
        main(SEED)
