from models.collaborative import DependencyFinder
from models.nn_config import Config
from utils.files_io import load_json
from models.neural_network import NNModelPredictor
from models.collaborative import BaselineModelPredictor

DEFAULT_RECOMMENDATION_LEN = 6
CLEAN_PRODUCTS_PATH = 'data/neural_network/clean-products.json'


class RecommendationGenerator:

    def get_generated_recommendations(self, session):
        pass


class CollaborativeRecommendationGenerator(RecommendationGenerator):

    def __init__(self, recommendation_len=DEFAULT_RECOMMENDATION_LEN):
        self.model_predictor = BaselineModelPredictor()
        self.products = load_json(CLEAN_PRODUCTS_PATH)
        self.recommendation_len = recommendation_len

    def get_generated_recommendations(self, session):
        prediction = self.model_predictor.get_prediction(session)
        output = self._deserialise_collaborative_output(prediction)
        return sorted(output, key=lambda x: x[1], reverse=True)[:self.recommendation_len]

    def _get_prod_id_from_matrix_row(self, matrix_row):
        for i, prod in enumerate(self.products):
            if i == matrix_row:
                return prod['product_id']

    def _deserialise_collaborative_output(self, processed_prediction):
        deserialised_output = []
        for dependant_product in processed_prediction:
            for product in self.products:
                if self._get_prod_id_from_matrix_row(dependant_product[0]) == product['product_id']:
                    deserialised_output.append(
                        (product['product_name'], product['category_path'], dependant_product[1]))

        return deserialised_output


class NNRecommendationGenerator(RecommendationGenerator):

    def __init__(self, recommendation_len=DEFAULT_RECOMMENDATION_LEN):
        self.model_predictor = NNModelPredictor(Config())
        self.products = load_json(CLEAN_PRODUCTS_PATH)
        self.recommendation_len = recommendation_len

    def get_generated_recommendations(self, session):
        predictions = self.model_predictor.get_prediction(session)
        processed_predictions = self._process_nn_output(predictions)
        return self._deserialise_nn_output(processed_predictions)

    def _process_nn_output(self, predictions):
        processed_prediction = []
        for prediction in predictions:
            prediction_as_dict = {}
            for product_prediction, product in zip(prediction, self.products):
                product_id = product['product_id']
                prediction_as_dict[product_id] = product_prediction

            top_n_products = sorted(prediction_as_dict.items(), key=lambda x: x[1], reverse=True)[
                             :self.recommendation_len]
            processed_prediction.append(top_n_products)

        return processed_prediction

    def _deserialise_nn_output(self, processed_predictions, prediction_idx=0):
        view_processed_predictions = []
        for viewed_products in processed_predictions[prediction_idx]:
            for product in self.products:
                if int(viewed_products[0]) == product['product_id']:
                    view_processed_predictions.append(
                        (product['product_name'], product['category_path']))
        return view_processed_predictions
