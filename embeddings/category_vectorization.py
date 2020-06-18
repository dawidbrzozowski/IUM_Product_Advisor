from collections import defaultdict

from embeddings.category_to_tree import CategoryTree
from utils.files_io import load_json

CLEAN_USERS_PATH = 'data/clean-users.json'
CLEAN_PRODUCTS_PATH = 'data/clean-products.json'
N_MUL = 4
INIT_POINT = 1.0


class CategoryVectorizer:

    def __init__(self):
        self._tree = CategoryTree()
        self._leaf_vectors = self._prepare_vectorization_for_leafs()
        self._products = load_json(CLEAN_PRODUCTS_PATH)

    def get_vector_for_leaf(self, leaf_name):
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

