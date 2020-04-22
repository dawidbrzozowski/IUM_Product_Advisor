from utils.files_io import load_jsonl
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
        pass


def main():
    p = Preprocessor()
    p.clean_products()


if __name__ == '__main__':
    main()
