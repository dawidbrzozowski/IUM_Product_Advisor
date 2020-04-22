from utils.files_io import load_jsonl, write_json_file
import pandas as pd

USERS_PATH = 'data/users.jsonl'
SESSIONS_PATH = 'data/sessions.jsonl'
PRODUCTS_PATH = 'data/products.jsonl'

USER_UNNECESSARY_ATTRIBUTES = ['street', 'name']

MIN_POSSIBLE_VALUE = 0
MAX_POSSIBLE_VALUE = 100000

N_SIGMA = 3


class Preprocessor:

    def __init__(self):
        self.products = load_jsonl(PRODUCTS_PATH)
        self.sessions = load_jsonl(SESSIONS_PATH)
        self.users = load_jsonl(USERS_PATH)
        # Narazie mysle, ze deliveries sa nam totalnie niepotrzebne. Jak zmienimy zdanie to je dodamy.

    def clean_users(self, unnecessary_attributes: list):
        return [self.get_user_without_unnecessary_data(user, unnecessary_attributes) for user in self.users]

    def get_user_without_unnecessary_data(self, user: dict, unnecessary_attributes: list):
        for attribute in unnecessary_attributes:
            user.pop(attribute)
        return user

    def clean_products(self):
        products = self.get_products_with_possible_price(self.products)
        products_df = pd.DataFrame(products)
        means = products_df[['category_path', 'price']].groupby('category_path').mean()
        stds = products_df[['category_path', 'price']].groupby('category_path').std()
        stds = stds.fillna(0)
        products = self.get_products_within_sigma_n(products, means, stds, N_SIGMA)
        return products

    def get_products_with_possible_price(self, products):
        cleaned_products = []
        for product in products:
            if MIN_POSSIBLE_VALUE < product['price'] < MAX_POSSIBLE_VALUE:
                cleaned_products.append(product)
        return cleaned_products

    def get_products_within_sigma_n(self, products, means, stds, n):
        products_within_sigma = []
        for product in products:
            min_value = means.loc[product['category_path']]['price'] - n * stds.loc[product['category_path']]['price']
            max_value = means.loc[product['category_path']]['price'] + n * stds.loc[product['category_path']]['price']
            if min_value < product['price'] < max_value:
                products_within_sigma.append(product)
        return products_within_sigma

    def clean_sessions(self):
        sessions = self.fill_missing_user_id(self.sessions)
        sessions = self.drop_sessions_with_empty_user_id(sessions)
        sessions = self.drop_sessions_with_empty_product_id(sessions)
        sessions = self.drop_buy_sessions_without_purchase_id(sessions)
        write_json_file('temp', sessions)

    def fill_missing_user_id(self, sessions):
        for i, session in enumerate(sessions):
            if session['user_id'] is None:
                if self.get_prev_not_null_user_id(sessions, i) == self.get_next_not_null_user_id(sessions, i):
                    session['user_id'] = self.get_next_not_null_user_id(sessions, i)
                elif self.get_prev_not_null_session_id(sessions, i) == session['session_id']:
                    session['user_id'] = self.get_prev_not_null_user_id(sessions, i)
                elif self.get_next_not_null_session_id(sessions, i) == session['session_id']:
                    session['user_id'] = self.get_next_not_null_user_id(sessions, i)
        return sessions

    def drop_sessions_with_empty_user_id(self, sessions):
        return [session for session in sessions if session['user_id'] is not None]

    def drop_sessions_with_empty_product_id(self, sessions):
        return [session for session in sessions if session['product_id'] is not None]

    def drop_buy_sessions_without_purchase_id(self, sessions):
        return [session for session in sessions if not
        (session['event_type'] == 'BUY_PRODUCT' and session['purchase_id'] is None)]

    def drop_sessions_without_timestamp(self, sessions):
        return [session for session in sessions if session['timestamp'] is not None]

    def get_prev_not_null_user_id(self, sessions, i):
        while i >= 0 and sessions[i]['user_id'] is None:
            i -= 1
        return sessions[i]['user_id']

    def get_next_not_null_user_id(self, sessions, i):
        while i < len(sessions) and sessions[i]['user_id'] is None:
            i += 1
        return sessions[i]['user_id']

    def get_prev_not_null_session_id(self, sessions, i):
        while i >= 0 and sessions[i]['user_id'] is None:
            i -= 1
        return sessions[i]['session_id']

    def get_next_not_null_session_id(self, sessions, i):
        while i < len(sessions) and sessions[i]['user_id'] is None:
            i += 1
        return sessions[i]['session_id']


def main():
    p = Preprocessor()
    p.clean_sessions()


if __name__ == '__main__':
    main()
