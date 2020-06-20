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


X_train = load_json('data/neural_network/X_train.json')
y_train = load_json('data/neural_network/y_train.json')
X_train = pd.DataFrame(X_train)
y_train = pd.DataFrame(y_train)
X_train.drop(columns=['session_id'], inplace=True)
y_train.drop(columns=['session_id'], inplace=True)
print(y_train)

X_test = load_json('data/neural_network/X_test.json')
X_test_to_compare = X_test.copy()
X_test = pd.DataFrame(X_test)
X_test.drop(columns=['session_id'], inplace=True)
model_trainer = NNModelTrainer(288, 275)
model_trainer.train(X_train, y_train, 100, 5)
prediction = model_trainer.model.predict(X_test)

clean_products = load_json('data/neural_network/clean-products.json')


def get_prod_id_from_network_column_id(network_id, products):
    for i, prod in enumerate(products):
        if i == network_id:
            return prod['product_id']


results_to_show = 8
processed_prediction = []
for single_pred in prediction:
    single_dict_pred = {}
    for i, single_pred_for_product in enumerate(single_pred):
        product_id = get_prod_id_from_network_column_id(i, clean_products)
        single_dict_pred[product_id] = single_pred_for_product

    sorted_single_pred = sorted(single_dict_pred.items(), key=lambda x: x[1], reverse=True)
    sorted_single_pred_top_n = sorted_single_pred[:results_to_show]
    processed_prediction.append(sorted_single_pred_top_n)

row_id = 1
first_prod_column = 3
last_prod_column_exclusive = len(X_test_to_compare[row_id]) - 11
# temporary
view = []
print(len(X_test_to_compare[row_id]))
for i, product_in_session in enumerate(X_test_to_compare[row_id]):
    # print(type(X_test_to_compare[row_id]))
    if first_prod_column <= i < last_prod_column_exclusive and \
            X_test_to_compare[row_id][product_in_session] != 0:
        view.append(product_in_session)

print(X_test_to_compare[row_id]['session_id'])

view_names = []
for vied_product_id in view:
    for product in clean_products:
        if int(vied_product_id) == product['product_id']:
            print('matched')
            view_names.append((product['product_name'], product['category_path']))

view_processed_predictions = []
for vied_product_id in processed_prediction[row_id]:
    # print(vied_product_id[0], vied_product_id[1], type(vied_product_id))
    for product in clean_products:
        if int(vied_product_id[0]) == product['product_id']:
            print('matched')
            view_processed_predictions.append((product['product_name'], product['category_path'], vied_product_id[1]))

print('obejrzano: ')
for item in view_names:
    print(item)

print('polecono: ')
for item in view_processed_predictions:
    print(item[0], '\t\t', item[1], '\t', item[2])

# prediction = [get_idx_of_predictions_over_threshold(0.02, pred) for pred in prediction]
# print(prediction)
