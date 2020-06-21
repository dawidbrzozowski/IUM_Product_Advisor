from models.collaborative import DependencyFinder
from models.nn_config import Config
from utils.files_io import load_json
from models.neural_network import NNModelPredictor

DEFAULT_RECOMMENDATION_LEN = 6
CLEAN_PRODUCTS_PATH = 'data/neural_network/clean-products.json'


class RecommendationGenerator:

    def get_generated_recommendations(self, session):
        pass


class CollaborativeRecommendationGenerator(RecommendationGenerator):

    def __init__(self, products, sessions):
        self.generated_recommendation = None
        self.dependency_finder = DependencyFinder(products)
        self.sessions = sessions

    def generate_recommendation(self, session):
        self.dependency_finder.parse_sessions_to_find_dependencies(self.sessions)
        dependencies = self.dependency_finder.dependencies


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
                        (product['product_name'], product['category_path'], viewed_products[1]))
        return view_processed_predictions
