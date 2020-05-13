from utils.files_io import load_json
import numpy as np


def load_sessions_data():
    return load_json('data/clean-sessions.json')


def get_products_data_size():
    return len(load_json('data/clean-products.json'))


class ProductDependecies:

    def __init__(self, products):
        self.products = products
        self.product_id_to_idx, self.idx_to_product_id = self._init_mappers()
        matrix_edge_size = len(self.products)
        self.matrix = self._init_empty_matrix(matrix_edge_size)

    def _init_mappers(self):
        product_id_to_idx = {}
        idx_to_product_id = {}
        for i, product in enumerate(self.products):
            product_id_to_idx[product['product_id']] = i
            idx_to_product_id[i] = product['product_id']
        return product_id_to_idx, idx_to_product_id

    def _init_empty_matrix(self, length):
        return np.zeros((length, length))

    def add(self, viewed_product, bought_product):
        viewed_product_idx = self.product_id_to_idx[viewed_product]
        bought_product_idx = self.product_id_to_idx[bought_product]
        self.matrix[viewed_product_idx, bought_product_idx] += 1


class SessionProducts:
    def __init__(self):
        self.products = {
            'VIEW_PRODUCT': [],
            'BUY_PRODUCT': []
        }

    def append(self, event, product):
        self.products[event].append(product)

    def clear(self):
        for event_type in self.products:
            self.products[event_type].clear()

    def add_to_dependency(self, dependencies):
        for bought_product in self.products['BUY_PRODUCT']:
            for viewed_product in self.products['VIEW_PRODUCT']:
                dependencies.add(viewed_product, bought_product)


class DependencyFinder:

    def __init__(self, products):
        self.dependencies = ProductDependecies(products)
        self.session_products = SessionProducts()

    def _move_session_info_to_dependencies(self):
        self.session_products.add_to_dependency(self.dependencies)
        self.session_products.clear()

    def parse_sessions_to_find_dependencies(self, sessions):
        current_session_id = 0
        for session in sessions:
            next_session_id = session['session_id']

            if current_session_id == next_session_id:
                self._gather_session_info(session)
            else:
                self._move_session_info_to_dependencies()
            current_session_id = next_session_id

    def _gather_session_info(self, session):
        current_event = session['event_type']
        current_product = session['product_id']
        self.session_products.append(current_event, current_product)


def main():
    clean_products = load_json("data/clean-products.json")
    clean_sessions = load_json("data/clean-sessions.json")

    pm = DependencyFinder(clean_products)
    pm.parse_sessions_to_find_dependencies(clean_sessions)
    print(pm.dependencies.matrix.sum())


if __name__ == '__main__':
    main()
