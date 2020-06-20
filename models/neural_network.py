from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Nadam


class NNModelTrainer:

    def __init__(self, config):
        self.config = config
        self.model = self._init_model(self.config.hidden_layer_size)

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


class NNModelPredictor:
    def get_prediction(self):
        pass
