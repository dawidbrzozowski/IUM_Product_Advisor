from collections import defaultdict
from embeddings.category_to_tree import CategoryTree
from utils.files_io import load_json

CLEAN_USERS_PATH = 'data/clean-users.json'
CLEAN_PRODUCTS_PATH = 'data/clean-products.json'
N_MUL = 4
INIT_POINT = 1.0


class Vectorizer:

    def prepare_products(self, products):
        products = self._normalize_prices(products)
        return self._vectorize_product_categories(products)

    def _vectorize_product_categories(self, products):
        products_with_vectorized_category = []
        category_vectorizer = CategoryVectorizer(products)
        for product in products:
            product['category_path'] = category_vectorizer.get_vector_for_category_path(product['category_path'])
            products_with_vectorized_category.append(products)
        return products_with_vectorized_category

    def _normalize_prices(self, products):
        # todo normalizacja
        return products


class CategoryVectorizer:

    def __init__(self, products):
        self._tree = CategoryTree(products)
        self._leaf_vectors = self._prepare_vectorization_for_leafs()
        self._products = products

    def get_vector_for_category_path(self, category_path):
        leaf_name = self._tree.get_leaf_from_category_path(category_path)
        return self._leaf_vectors.get(leaf_name)

    def _prepare_vectorization_for_leafs(self):
        leafs_as_vectors = {}
        for leaf in self._tree.get_all_leafs():
            leafs_as_vectors[leaf] = self._prepare_vectorization_for_leaf(leaf)
        return leafs_as_vectors

    def _prepare_vectorization_for_leaf(self, leaf, n_mul=N_MUL):
        category_weights = defaultdict(float)
        point = INIT_POINT
        normalization_sum = 0
        for node in self._tree.get_path_to_leaf(leaf):
            for descendant in self._tree.get_descendants_of_node(node):
                category_weights[descendant] += point
                normalization_sum += point
            point *= n_mul
        for weight in category_weights:
            category_weights[weight] /= normalization_sum
        return list(category_weights.values())
