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


class BaselineModelPredictor:

    def get_prediction(self, session):
        viewed_products_in_session = self._get_viewed_products_in_session(session)
        clean_products = load_json("data/baseline/clean-products.json")
        viewed_products_as_rows = self._get_matrix_row_ids_from_product_ids(viewed_products_in_session, clean_products)

        clean_sessions = load_json("data/baseline/clean-sessions.json")
        pm = DependencyFinder(clean_products)
        pm.parse_sessions_to_find_dependencies(clean_sessions)

        deps = self._get_dependand_columns_to_given_rows(viewed_products_as_rows, pm.dependencies.matrix)
        return deps

    def _is_in_dep(self, i, deep_dependant_products):
        for elem in deep_dependant_products:
            if elem[0] == i:
                return True
        return False

    def _get_dependand_columns_to_given_rows(self, viewed_products_as_rows, matrix):
        dependency_depth = 3
        deep_dependant_products = []
        for i in range(dependency_depth):
            dependant_products = {}
            viewed_products_as_rows_for_given_depth = viewed_products_as_rows
            viewed_products_as_rows = []

            for single_row in matrix[viewed_products_as_rows_for_given_depth]:
                for i, dependency_for_row in enumerate(single_row):
                    if dependency_for_row != 0 and not self._is_in_dep(i, deep_dependant_products):
                        if i in dependant_products:
                            dependant_products[i] += dependency_for_row
                            viewed_products_as_rows.append(i)
                        else:
                            dependant_products[i] = 0

            dependant_products_by_quality = sorted(dependant_products.items(), key=lambda x: x[1], reverse=True)
            deep_dependant_products += dependant_products_by_quality

        # then add products mostly viewed in general
        mostly_viewed_with_no_dep = {}
        for single_row in matrix:
            for i, single_cell in enumerate(single_row):
                if single_cell != 0 and not self._is_in_dep(i, deep_dependant_products):
                    if i in mostly_viewed_with_no_dep:
                        mostly_viewed_with_no_dep[i] += single_cell
                    else:
                        mostly_viewed_with_no_dep[i] = 0

        mostly_viewed_with_no_dep_by_quality = sorted(mostly_viewed_with_no_dep.items(),
                                                      key=lambda x: x[1], reverse=True)
        return deep_dependant_products + mostly_viewed_with_no_dep_by_quality

    def _get_viewed_products_in_session(self, session):
        view = []
        first_prod_column = 3
        last_prod_column_exclusive = len(session) - 12
        for i, product_in_session in enumerate(session):
            if first_prod_column <= i < last_prod_column_exclusive and \
                    session[product_in_session] != 0:
                view.append(product_in_session)

        return view

    def _get_matrix_row_ids_from_product_ids(self, viewed_products_in_session, products):
        matrix_rows = []
        for viewed_product in viewed_products_in_session:
            matrix_row = self._get_matrix_row_from_column_id(viewed_product, products)
            matrix_rows.append(matrix_row)

        return matrix_rows

    def _get_matrix_row_from_column_id(self, viewed_product, products):
        for i, prod in enumerate(products):
            if prod['product_id'] == int(viewed_product):
                return i
