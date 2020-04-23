from utils.files_io import load_jsonl, write_json_file
import pandas as pd

DEFAULT_USERS_PATH = 'data/users.jsonl'
DEFAULT_SESSIONS_PATH = 'data/sessions.jsonl'
DEFAULT_PRODUCTS_PATH = 'data/products.jsonl'

SAVE_DIR = 'data/'

USER_UNNECESSARY_ATTRIBUTES = ['street', 'name']

MIN_POSSIBLE_VALUE = 0
MAX_POSSIBLE_VALUE = 100000

N_SIGMA = 3


class Preprocessor:

    def clean_users(self, users, unnecessary_attributes: list):
        return [self._get_user_without_unnecessary_data(user, unnecessary_attributes) for user in users]

    def _get_user_without_unnecessary_data(self, user: dict, unnecessary_attributes: list):
        for attribute in unnecessary_attributes:
            user.pop(attribute)
        return user

    def clean_products(self, products):
        products = self._get_products_with_possible_price(products)
        products_df = pd.DataFrame(products)
        means = products_df[['category_path', 'price']].groupby('category_path').mean()
        stds = products_df[['category_path', 'price']].groupby('category_path').std()
        stds = stds.fillna(0)
        products = self._get_products_within_sigma_n(products, means, stds, N_SIGMA)
        return products

    def _get_products_with_possible_price(self, products):
        cleaned_products = []
        for product in products:
            if MIN_POSSIBLE_VALUE < product['price'] < MAX_POSSIBLE_VALUE:
                cleaned_products.append(product)
        return cleaned_products

    def _get_products_within_sigma_n(self, products, means, stds, n):
        products_within_sigma = []
        for product in products:
            min_value = means.loc[product['category_path']]['price'] - n * stds.loc[product['category_path']]['price']
            max_value = means.loc[product['category_path']]['price'] + n * stds.loc[product['category_path']]['price']
            if min_value < product['price'] < max_value:
                products_within_sigma.append(product)
        return products_within_sigma

    def clean_sessions(self, sessions):
        sessions = self._fill_missing_user_id_where_possible(sessions)
        sessions = self._drop_sessions_without_user_id(sessions)
        sessions = self._drop_sessions_without_product_id(sessions)
        sessions = self._drop_buy_sessions_without_purchase_id(sessions)
        return sessions

    def _fill_missing_user_id_where_possible(self, sessions):
        for i, session in enumerate(sessions):
            if session['user_id'] is None:
                session['user_id'] = self._find_user_id_from_neighbours(sessions, i)
        return sessions

    def _find_user_id_from_neighbours(self, sessions, i):
        # jezeli poprzedni rekord ma taki sam user_id jak nastepny, to wpisz ten user_id
        if self._get_prev_not_null_user_id(sessions, i) == self._get_next_not_null_user_id(sessions, i):
            return self._get_next_not_null_user_id(sessions, i)
        # jezeli id sesji poprzedniego rekordu jest takie samo, to znaczy, ze musi to byc ten sam user_id
        if self._get_prev_not_null_session_id(sessions, i) == sessions[i]['session_id']:
            return self._get_prev_not_null_user_id(sessions, i)
        # jezeli id sesji nastepnego rekordu jest takie samo, to znaczy, ze musi byc to ten sam user_id
        if self._get_next_not_null_session_id(sessions, i) == sessions[i]['session_id']:
            return self._get_next_not_null_user_id(sessions, i)
        return None

    def _drop_sessions_without_user_id(self, sessions):
        return [session for session in sessions if session['user_id'] is not None]

    def _drop_sessions_without_product_id(self, sessions):
        return [session for session in sessions if session['product_id'] is not None]

    def _drop_buy_sessions_without_purchase_id(self, sessions):
        return [session for session in sessions if not
        (session['event_type'] == 'BUY_PRODUCT' and session['purchase_id'] is None)]

    def _drop_sessions_without_timestamp(self, sessions):
        return [session for session in sessions if session['timestamp'] is not None]

    def _get_prev_not_null_user_id(self, sessions, i):
        while i >= 0 and sessions[i]['user_id'] is None:
            i -= 1
        return sessions[i]['user_id']

    def _get_next_not_null_user_id(self, sessions, i):
        while i < len(sessions) and sessions[i]['user_id'] is None:
            i += 1
        return sessions[i]['user_id']

    def _get_prev_not_null_session_id(self, sessions, i):
        while i >= 0 and sessions[i]['user_id'] is None:
            i -= 1
        return sessions[i]['session_id']

    def _get_next_not_null_session_id(self, sessions, i):
        while i < len(sessions) and sessions[i]['user_id'] is None:
            i += 1
        return sessions[i]['session_id']


def read_users_sessions_products(users_path=DEFAULT_USERS_PATH, sessions_path=DEFAULT_SESSIONS_PATH,
                                 products_path=DEFAULT_PRODUCTS_PATH):
    users = load_jsonl(users_path)
    sessions = load_jsonl(sessions_path)
    products = load_jsonl(products_path)
    return users, sessions, products


def save_clean_data(users, sessions, products, save_dir):
    preprocessor = Preprocessor()
    clean_users = preprocessor.clean_users(users, USER_UNNECESSARY_ATTRIBUTES)
    clean_sessions = preprocessor.clean_sessions(sessions)
    clean_products = preprocessor.clean_products(products)

    write_json_file(save_dir + 'clean-users', clean_users)
    write_json_file(save_dir + 'clean-sessions', clean_sessions)
    write_json_file(save_dir + 'clean-products', clean_products)


def main():
    users, sessions, products = read_users_sessions_products()
    save_clean_data(users, sessions, products, SAVE_DIR)


if __name__ == '__main__':
    main()
