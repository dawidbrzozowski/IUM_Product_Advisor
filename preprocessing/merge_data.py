import pandas as pd

from utils.files_io import write_json_file

CLEAN_USERS_PATH = 'data/clean-users.json'
CLEAN_SESSIONS_PATH = 'data/clean-sessions.json'
CLEAN_PRODUCTS_PATH = 'data/clean-products.json'


def read_df_users_sessions_products(users_path=CLEAN_USERS_PATH, sessions_path=CLEAN_SESSIONS_PATH,
                                    products_path=CLEAN_PRODUCTS_PATH):
    users = pd.read_json(users_path)
    sessions = pd.read_json(sessions_path)
    products = pd.read_json(products_path)
    return users, sessions, products


def merge(users: pd.DataFrame, sessions: pd.DataFrame, products: pd.DataFrame):
    merged = sessions.merge(users, on='user_id').merge(products, on='product_id')
    merged = merged.astype({'timestamp': 'str'})
    return merged.to_dict(orient='records')


if __name__ == '__main__':
    users_df, sessions_df, products_df = read_df_users_sessions_products()
    merged = merge(users_df, sessions_df, products_df)
    write_json_file('data/merged-data', merged)
