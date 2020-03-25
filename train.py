# https://www.tensorflow.org/tutorials/structured_data/time_series

import tensorflow as tf

import preprocessor

past_history = 720
future_target = 72
STEP = 6

def train():

    # set seed to ensure reproducability
    tf.random.set_seed(64)


    # parse data from CSV files and process
    features = preprocessor.get_data()

    # normalise
    dataset = features.values
    data_mean = dataset[:TRAIN_SPLIT].mean(axis=0)
    data_std = dataset[:TRAIN_SPLIT].std(axis=0)

    dataset = (dataset-data_mean)/data_std

    # reshape data into history chunk to consider and future chunk to predict
    # also these two functions split the dataset into training and validation sets
    x_train_single, y_train_single = preprocessor.multivariate_data(dataset, dataset[:, 1], 0,
                                                   TRAIN_SPLIT, past_history,
                                                   future_target, STEP,
                                                   single_step=True)

    x_val_single, y_val_single = preprocessor.multivariate_data(dataset, dataset[:, 1],
                                                TRAIN_SPLIT, None, past_history,
                                                future_target, STEP,
                                                single_step=True)

    # convert numpy arrays into tf.Dataset
    train_data_single = tf.data.Dataset.from_tensor_slices((x_train_single, y_train_single))
    # shuffle and form into batches
    # cache to speed up processing
    # repeat sets up the epoch feeding
    train_data_single = train_data_single.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

    # again with validation set
    # we don't need to shuffle the validation dataset as it is not being trained on, and therefore time dependent correlations can stay
    val_data_single = tf.data.Dataset.from_tensor_slices((x_val_single, y_val_single))
    val_data_single = val_data_single.batch(BATCH_SIZE).repeat()

    # define model
    # using two layers of LSTMs
    # using ReLU activation function
    multi_step_model = tf.keras.models.Sequential()
    multi_step_model.add(tf.keras.layers.LSTM(32,
                                            return_sequences=True,
                                            input_shape=x_train_multi.shape[-2:]))
    multi_step_model.add(tf.keras.layers.LSTM(16, activation='relu'))
    multi_step_model.add(tf.keras.layers.Dense(72))

    # using RMS
    multi_step_model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')

    multi_step_history = multi_step_model.fit(train_data_multi, epochs=EPOCHS,
                                          steps_per_epoch=EVALUATION_INTERVAL,
                                          validation_data=val_data_multi,
                                          validation_steps=50)

    plot_train_history(multi_step_history, 'Multi-Step Training and validation loss')

    for x, y in val_data_multi.take(3):
        multi_step_plot(x[0], y[0], multi_step_model.predict(x)[0])


if __name__ == "__main__":
    train()
