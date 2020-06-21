from embeddings.vectorization import Vectorizer
from utils.files_io import load_json, write_json_file

DEFAULT_AGE = 0.5
PRODUCTS_VECTORIZED_PATH = 'data/neural_network/products_vectorized_repr.json'
CLEAN_PRODUCTS_PATH = 'data/neural_network/clean-products.json'


class SessionRecommendationPreprocessor:
    def __init__(self):
        self.clean_products = load_json(CLEAN_PRODUCTS_PATH)

    def create_product_representation_for_web_app(self):
        return [f'{product["product_name"]}:{product["category_path"]}' for product in self.clean_products]

    def web_app_product_representation_to_product_ids(self, products):
        product_ids = []
        for product_repr in products:
            product_name = product_repr.split(':')[0]
            for product in self.clean_products:
                if product['product_name'] == product_name:
                    product_ids.append(product['product_id'])
        return product_ids

    def prepare_products_vectorized(self, cleaned_products):
        vectorizer = Vectorizer()
        products_vectorized = vectorizer.prepare_products(cleaned_products)
        product_ids = [product['product_id'] for product in cleaned_products]
        product_representation = {product_id: 0 for product_id in product_ids}

        products_with_id_as_key = {}
        for product in products_vectorized:
            product_id = product.pop('product_id')
            product.pop('category_path')
            product.pop('product_name')
            product['vectorized_product_id'] = product_representation.copy()
            product['vectorized_product_id'][product_id] += 1
            products_with_id_as_key[product_id] = product
        return products_with_id_as_key

    def preprocess(self, viewed_products_ids: list):
        product_repr = load_json(PRODUCTS_VECTORIZED_PATH)
        sum_session = None
        for product_id in viewed_products_ids:
            sum_session = self._add_products(sum_session, product_repr[str(product_id)])
        return self._get_average_session_from_products_sum(sum_session)

    def _get_average_session_from_products_sum(self, sum_session):
        avg_session = sum_session
        product_ids_vectorized = avg_session.pop('vectorized_product_id')
        for product_id in product_ids_vectorized:
            avg_session[product_id] = product_ids_vectorized[product_id]
        leafs = avg_session.pop('leafs')
        for leaf in leafs:
            avg_session[leaf] = leafs[leaf]
        avg_session['age'] = DEFAULT_AGE
        return avg_session

    def _add_products(self, product1: dict, product2: dict):
        if product1 is None and product2 is not None:
            return product2
        elif product1 is not None and product2 is None:
            return product1
        elif product1 is None and product2 is None:
            return None
        else:
            for leaf in product1['leafs']:
                product1['leafs'][leaf] += product2['leafs'][leaf]
            for product_id in product1['vectorized_product_id']:
                product1['vectorized_product_id'][product_id] += product2['vectorized_product_id'][product_id]
            return product1


if __name__ == '__main__':
    srp = SessionRecommendationPreprocessor()
    products_vectorized = srp.prepare_products_vectorized(load_json(CLEAN_PRODUCTS_PATH))
    write_json_file(PRODUCTS_VECTORIZED_PATH, products_vectorized)
