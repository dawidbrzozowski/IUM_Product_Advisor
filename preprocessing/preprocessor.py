from utils.files_io import load_jsonl, write_json_file
import pandas as pd

SAVE_DIR = 'data/'

DEFAULT_USERS_PATH = SAVE_DIR + 'users.jsonl'
DEFAULT_SESSIONS_PATH = SAVE_DIR + 'sessions.jsonl'
DEFAULT_PRODUCTS_PATH = SAVE_DIR + 'products.jsonl'

USER_UNNECESSARY_ATTRIBUTES = ['street', 'name']
SESSION_ATTRIBUTES_THAT_CANNOT_HAVE_NULL = ['user_id', 'product_id']

MIN_POSSIBLE_VALUE = 0
MAX_POSSIBLE_VALUE = 100000

N_SIGMA = 3

class Preprocessor:

    def clear_data(self, users, sessions, products):
        return self._clear_users(users), self._clear_sessions(sessions), self._clear_products(products)

    def _clear_users(self, users):
        for user in users:
            for attribute in USER_UNNECESSARY_ATTRIBUTES:
                user.pop(attribute)
        return users

    def _clear_products(self, products):
        products_prefiltered = self._remove_products_with_forbidden_values(products)
        return self._remove_products_using_n_sigma(products_prefiltered)

    def _remove_products_with_forbidden_values(self, products):
        return [product for product in products if MIN_POSSIBLE_VALUE <= product['price'] <= MAX_POSSIBLE_VALUE]

    def _remove_products_using_n_sigma(self, products):

        products_df = pd.DataFrame(products)
        products_groupped_by_cathegory_path = products_df[['category_path', 'price']].groupby('category_path')
        means = products_groupped_by_cathegory_path.mean()
        stds = products_groupped_by_cathegory_path.std().fillna(0)

        products_within_sigma = []
        for product in products:
            current_mean = means.loc[product['category_path']]['price']
            current_n_std = N_SIGMA * stds.loc[product['category_path']]['price']
            if  -current_n_std < product['price'] - current_mean < current_n_std:
                products_within_sigma.append(product)
        return products_within_sigma

    def _clear_sessions(self, sessions):
        sessions = self._fill_missing_user_id_where_possible(sessions)
        sessions = self._drop_sessions_with_none(sessions, 'user_id')
        sessions = self._drop_sessions_with_none(sessions, 'product_id')
        sessions = self._drop_buy_sessions_without_purchase_id(sessions)
        return sessions
    
    def _fill_missing_user_id_where_possible(self, sessions):
        for i, session in enumerate(sessions):
            if session['user_id'] is None:
                # ustaw wartosc sesji na podstawie sasiadow
                session['user_id'] = self._find_user_id_from_neighbours(sessions, i)
        return sessions

    def _find_user_id_from_neighbours(self, sessions, i):
        prev_not_null_user_id = self._get_prev_not_null_user_id(sessions, i)
        next_not_null_user_id = self._get_next_not_null_user_id(sessions, i)
    
        # jezeli poprzedni rekord ma taki sam user_id jak nastepny, to wpisz ten user_id
        if prev_not_null_user_id == next_not_null_user_id:
            return next_not_null_user_id

        # jezeli id sesji poprzedniego rekordu jest takie samo, to znaczy, ze musi to byc ten sam user_id
        if  self._get_prev_not_null_session_id(sessions, i) == sessions[i]['session_id']:
            return prev_not_null_user_id

        # jezeli id sesji nastepnego rekordu jest takie samo, to znaczy, ze musi byc to ten sam user_id
        if self._get_next_not_null_session_id(sessions, i) == sessions[i]['session_id']:
            return next_not_null_user_id
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

def read_data(users_path=DEFAULT_USERS_PATH, sessions_path=DEFAULT_SESSIONS_PATH,
                                 products_path=DEFAULT_PRODUCTS_PATH):
    users = load_jsonl(users_path)
    sessions = load_jsonl(sessions_path)
    products = load_jsonl(products_path)
    return users, sessions, products
    
def write_data(clean_users, clean_sessions, clean_products):
    write_json_file(SAVE_DIR + 'clean-users', clean_users)
    write_json_file(SAVE_DIR + 'clean-sessions', clean_sessions)
    write_json_file(SAVE_DIR + 'clean-products', clean_products)

def main():
    users, sessions, products = read_data()
    preprocessor = Preprocessor()
    clean_users, clean_sessions, clean_products = preprocessor.clear_data(users, sessions, products)
    write_data(clean_users, clean_sessions, clean_products)


if __name__ == '__main__':
    main()
