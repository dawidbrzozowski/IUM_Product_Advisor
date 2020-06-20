from models.collaborative import DependencyFinder
from models.nn_config import Config
from utils.files_io import load_json
from models.neural_network import NNModelPredictor


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

    def __init__(self, recommendation_len=6):
        self.model_predictor = NNModelPredictor(Config())
        self.current_recommendation = None
        self.products = load_json('data/neural_network/clean-products.json')
        self.recommendation_len = recommendation_len

    def get_generated_recommendations(self, session):
        prediction = self.model_predictor.get_prediction(session)
        processed_prediction = self._process_nn_output(prediction)
        return self._deserialise_nn_output(processed_prediction)

    def _get_prod_id_from_column_id(self, column_id):
        for i, prod in enumerate(self.products):
            if i == column_id:
                return prod['product_id']

    def _process_nn_output(self, prediction):
        processed_prediction = []
        for single_pred in prediction:
            single_dict_pred = {}
            for i, single_pred_for_product in enumerate(single_pred):
                product_id = self._get_prod_id_from_column_id(i)
                single_dict_pred[product_id] = single_pred_for_product

            sorted_single_pred = sorted(single_dict_pred.items(), key=lambda x: x[1], reverse=True)
            sorted_single_pred_top_n = sorted_single_pred[:self.recommendation_len]
            processed_prediction.append(sorted_single_pred_top_n)

        return processed_prediction

    def _deserialise_nn_output(self, processed_prediction, row_id=0):
        view_processed_predictions = []
        for viewed_products in processed_prediction[row_id]:
            for product in self.products:
                if int(viewed_products[0]) == product['product_id']:
                    view_processed_predictions.append(
                        (product['product_name'], product['category_path'], viewed_products[1]))

        return view_processed_predictions
#
#
# session = load_json('data/neural_network/test_session.json')
# recommendation_generator = NNRecommendationGenerator(session)
# recommendation = recommendation_generator.get_generated_recommendations()
# print(recommendation)
