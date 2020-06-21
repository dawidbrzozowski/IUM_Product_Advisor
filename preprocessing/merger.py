import pandas as pd


class Merger:

    def create_model_input(self, sessions, products):
        sessions = pd.DataFrame(sessions)
        products = pd.DataFrame(products)

        merged = sessions.merge(products, on='product_id')
        merged.sort_values(by=['session_id'], inplace=True)
        merged_cleaned = merged.drop(
            columns=['purchase_id', 'product_name', 'offered_discount', 'user_id'])
        return merged_cleaned.to_dict(orient='records')

    def get_bought_from_session(self, session_id, y):
        for y_row in y:
            if session_id == y_row['session_id']:
                return y_row['product_id']

    def represent_session_as_single_row(self, merged_data, y, clean_products):
        product_ids = [product['product_id'] for product in clean_products]
        product_representation = {product_id: 0 for product_id in product_ids}
        category_correlation = {category_leaf: 0 for category_leaf in merged_data[0]['leafs']}
        averaged_sessions = []
        current_session_id = -1
        current_session_avg = None
        bought_product_in_current_session = None

        for single_session in merged_data:
            if single_session['session_id'] != current_session_id:
                if current_session_id != -1:
                    current_session_avg.pop('product_id')
                    current_session_avg.pop('leafs')
                    current_session_avg.pop('category_path')
                    averaged_sessions.append(current_session_avg)

                bought_product_in_current_session = self.get_bought_from_session(single_session['session_id'], y)
                current_session_id = single_session['session_id']
                current_session_avg = single_session.copy()
                current_session_avg.update(product_representation)
                current_session_avg.update(category_correlation)

            product_id = single_session['product_id']
            if product_id != bought_product_in_current_session:
                current_session_avg[product_id] += 1
                for leaf in single_session['leafs']:
                    current_session_avg[leaf] += single_session['leafs'][leaf]

        current_session_avg.pop('product_id')
        current_session_avg.pop('leafs')
        current_session_avg.pop('category_path')
        averaged_sessions.append(current_session_avg)

        return averaged_sessions

    def represent_bought_products_as_matrix(self, y, clean_products):
        product_ids = [product['product_id'] for product in clean_products]
        product_representation = {product_id: 0 for product_id in product_ids}

        bought_product_representation = []
        for single_session in y:
            single_session.update(product_representation)
            bought_product_id = single_session.pop('product_id')
            single_session[bought_product_id] += 1
            bought_product_representation.append(single_session)

        return bought_product_representation

    # todo normalizacja kategorii i wystapien produktow

    def split_into_x_y(self, merged_data):
        X = []
        Y = []
        for row in merged_data:
            if row['event_type'] == 'BUY_PRODUCT':
                Y.append({'session_id': row['session_id'], 'product_id': row['product_id']})
            else:
                row.pop('event_type')
                X.append(row)
        return self.get_matching_x_y(X, Y)

    def get_matching_x_y(self, X, Y):
        y_sessions = set()
        for y in Y:
            y_sessions.add(y['session_id'])
        X_match = []
        for x in X:
            if x['session_id'] in y_sessions:
                X_match.append(x)

        x_sessions = set()
        Y_match = []
        for x in X_match:
            x_sessions.add(x['session_id'])
        for y in Y:
            if y['session_id'] in x_sessions:
                Y_match.append(y)
        return X_match, Y_match
