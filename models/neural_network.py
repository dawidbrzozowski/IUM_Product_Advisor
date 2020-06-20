from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Nadam
import pandas as pd
from tensorflow.keras.callbacks import TensorBoard

from models.nn_config import Config
from utils.files_io import load_json

HIDDEN_LAYER_SIZE = 100


class NNModelTrainer:

    def __init__(self, config):
        self.config = config
        self.model = self._init_model(HIDDEN_LAYER_SIZE)

    def _init_model(self, hidden_layer_units):
        input_ = Input(shape=(self.config.input_shape,))
        y = Dense(units=hidden_layer_units, activation='relu')(input_)
        y = Dense(units=self.config.output_shape, activation='sigmoid')(y)
        model = Model(input_, y)
        model.compile(optimizer=Nadam(), loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        return model

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, validation_split=0.1,
                       callbacks=[self.config.callback], epochs=self.config.epochs, batch_size=self.config.batch_size)
        self.model.save(self.config.model_save_path)
        return self.model


class NNIO:
    def get_prediction(self):
        X_train = load_json('data/neural_network/X_train.json')
        y_train = load_json('data/neural_network/y_train.json')
        X_train = pd.DataFrame(X_train)
        y_train = pd.DataFrame(y_train)

        X_test = load_json('data/neural_network/X_test.json')
        X_test = pd.DataFrame(X_test)
        config = Config()
        model_trainer = NNModelTrainer(config)
        model_trainer.train(X_train, y_train)
        prediction = model_trainer.model.predict(X_test)
        return prediction
