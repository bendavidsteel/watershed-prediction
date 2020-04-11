# https://www.tensorflow.org/tutorials/structured_data/time_series

import os
import pickle

import pandas as pd
import skimage
import tensorflow as tf

import preprocessor

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "dataset")

def train():
    # set seed to ensure reproducability
    tf.random.set_seed(64)

    input_data = pd.read_csv(os.path.join(dataset_path, "all_data.csv"))

    # normalise
    dataset = input_data.drop(["Date"], axis=1).values
    TRAIN_SPLIT = int(0.8*len(dataset))
    data_mean = dataset[:TRAIN_SPLIT].mean(axis=0)
    data_std = dataset[:TRAIN_SPLIT].std(axis=0)
    dataset = (dataset-data_mean)/data_std
    inputs = dataset[:, 6:]
    targets = dataset[:, :6]

    # reshape data into history chunk to consider and future chunk to predict
    SEQUENCE_LENGTH = 60
    train_inputs_overlap = skimage.util.view_as_windows(inputs[:TRAIN_SPLIT], (SEQUENCE_LENGTH, 24)).reshape(-1, SEQUENCE_LENGTH, 24)
    train_targets_overlap = skimage.util.view_as_windows(targets[:TRAIN_SPLIT], (SEQUENCE_LENGTH, 6)).reshape(-1, SEQUENCE_LENGTH, 6)
    val_inputs_overlap = skimage.util.view_as_windows(inputs[TRAIN_SPLIT:], (SEQUENCE_LENGTH, 24)).reshape(-1, SEQUENCE_LENGTH, 24)
    val_targets_overlap = skimage.util.view_as_windows(targets[TRAIN_SPLIT:], (SEQUENCE_LENGTH, 6)).reshape(-1, SEQUENCE_LENGTH, 6)

    BATCH_SIZE = 32
    train_data = tf.data.Dataset.from_tensor_slices((train_inputs_overlap, train_targets_overlap))
    train_data = train_data.shuffle(len(train_inputs_overlap), reshuffle_each_iteration=True).batch(BATCH_SIZE)

    val_data = tf.data.Dataset.from_tensor_slices((val_inputs_overlap, val_targets_overlap))
    val_data = val_data.batch(BATCH_SIZE)

    # define model
    # using two layers of LSTMs
    # using ReLU activation function
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(64,
                            return_sequences=True),
        tf.keras.layers.LSTM(32,
                            return_sequences=True,
                            activation='relu'),
        tf.keras.layers.Dense(6)
    ])
    model.compile(optimizer='RMSprop', loss='mse')

    EPOCHS=1
    early_stopping = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    train_history = model.fit(train_data, epochs=EPOCHS,
                              validation_data=val_data, callbacks=[early_stopping],
                              verbose=1)

    model.save(os.getcwd())

    with open(os.path.join(os.getcwd(), "history.pkl"), 'wb') as history_file:
        pickle.dump(train_history.history, history_file)

if __name__ == "__main__":
    train()
