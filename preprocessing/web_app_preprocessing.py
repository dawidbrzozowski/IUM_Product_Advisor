from embeddings.vectorization import Vectorizer
from utils.files_io import load_json


class SessionRecommendationPreprocessor:

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

    def add(self, product1: dict, product2: dict):
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

    def sum_session_to_avg_session(self, sum_session):
        avg_session = sum_session
        product_ids_vectorized = avg_session.pop('vectorized_product_id')
        for product_id in product_ids_vectorized:
            avg_session[product_id] = product_ids_vectorized[product_id]
        leafs = avg_session.pop('leafs')
        for leaf in leafs:
            avg_session[leaf] = leafs[leaf]
        avg_session['age'] = 0.5
        return avg_session

    def preprocess(self, viewed_products_ids: list):
        product_repr = load_json('data/neural_network/product_repr.json')
        sum_session = None
        for product_id in viewed_products_ids:
            sum_session = self.add(sum_session, product_repr[product_id])
        return self.sum_session_to_avg_session(sum_session)
