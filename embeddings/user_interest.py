from collections import defaultdict

from embeddings.category_to_tree import CategoryTree
from utils.files_io import load_json

CLEAN_USERS_PATH = 'data/clean-users.json'
CLEAN_PRODUCTS_PATH = 'data/clean-products.json'
N_MUL = 4
INIT_POINT = 1.0


class UserInterest:

    def __init__(self):
        self.tree = CategoryTree()
        self.leaf2idx = self.tree.get_leaf2idx()
        self.leaf_vectors = self.prepare_vectorization_for_leafs()
        self.products = load_json(CLEAN_PRODUCTS_PATH)

    @staticmethod
    def get_count_of_dataset_at_path(path):
        dataset = load_json(path)
        return len(dataset)

    def prepare_vectorization_for_leafs(self):
        leafs_as_vectors = {}
        for leaf in self.tree.get_all_leafs():
            leafs_as_vectors[leaf] = self.prepare_vectorization_for_leaf(leaf)
        return leafs_as_vectors

    def prepare_vectorization_for_leaf(self, leaf):
        category_weights = defaultdict(float)
        point = INIT_POINT
        normalization_sum = 0
        for node in self.tree.get_path_to_leaf(leaf):
            for descendant in self.tree.get_descendants_of_node(node):
                category_weights[descendant] += point
                normalization_sum += point
            point *= N_MUL
        for weight in category_weights:
            category_weights[weight] /= normalization_sum
        return list(category_weights.values())

    def create_product_interest_from_category(self, product_category):
        products_vector = []
        for product in self.products:
            products_vector.append(self.leaf_vectors[product_category][self.leaf2idx[product['category_leaf']]])
        return len(products_vector)

    def prepare_interest_matrix_for_user(self, user_id):
        pass


if __name__ == '__main__':
    user_interest = UserInterest()
    sessions = load_json('data/clean-sessions.json')
    print(user_interest.create_product_interest_from_category("Gry komputerowe"))
