from keras.callbacks import TensorBoard

from utils.files_io import load_json

DEFAULT_SAVE_PATH = 'models/saved_models/model.h5'
NN_TEST_DATA_PATH = 'data/neural_network/X_test.json'
PRODUCTS_PATH = 'data/baseline/clean-products.json'


class Config:
    def __init__(self, model_save_path=DEFAULT_SAVE_PATH, epochs=20, batch_size=100, hidden_layer_size=128):
        self.model_save_path = model_save_path
        self.epochs = epochs
        self.batch_size = batch_size
        self.hidden_layer_size = hidden_layer_size
        self.input_shape = self._check_dataset_for_input_shape()
        self.output_shape = self._check_products_for_output_shape()
        self.callback = TensorBoard(log_dir="./logs")

    def _check_dataset_for_input_shape(self):
        nn_input_data = load_json(NN_TEST_DATA_PATH)
        return len(nn_input_data[0])

    def _check_products_for_output_shape(self):
        products = load_json(PRODUCTS_PATH)
        return len(products)
