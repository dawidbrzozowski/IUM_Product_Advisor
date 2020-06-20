from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Nadam
import pandas as pd
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
from utils.files_io import load_json

HIDDEN_LAYER_SIZE = 100


class NNModelTrainer:

    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = self._init_model(HIDDEN_LAYER_SIZE)

    def _init_model(self, hidden_layer_units):
        input_ = Input(shape=(self.input_shape,))
        y = Dense(units=hidden_layer_units, activation='relu')(input_)
        y = Dense(units=self.output_shape, activation='sigmoid')(y)
        model = Model(input_, y)
        model.compile(optimizer=Nadam(), loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        return model

    def train(self, X_train, y_train, batch_size, epochs):
        callback = TensorBoard(log_dir="./logs")

        self.model.fit(X_train, y_train, validation_split=0.1,
                       callbacks=[callback], epochs=epochs, batch_size=batch_size)
        self.model.save('models/saved_models/curr_model.h5')


def get_idx_of_predictions_over_threshold(threshold, prediction):
    indexes_over_threshold = []


X_train = load_json('data/neural_network/X_train.json')
y_train = load_json('data/neural_network/y_train.json')
X_train = pd.DataFrame(X_train)
y_train = pd.DataFrame(y_train)
X_train.drop(columns=['session_id'], inplace=True)
y_train.drop(columns=['session_id'], inplace=True)
print(y_train)

X_test = load_json('data/neural_network/X_test.json')
X_test = pd.DataFrame(X_test)
X_test.drop(columns=['session_id'], inplace=True)
model_trainer = NNModelTrainer(288, 275)
model_trainer.train(X_train, y_train, 100, 20)
prediction = model_trainer.model.predict(X_test)

prediction = [get_idx_of_predictions_over_threshold(0.02, pred) for pred in prediction]
print(prediction)
