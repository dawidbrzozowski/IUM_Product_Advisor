import pandas as pd
from utils.files_io import write_json_file

CLEAN_USERS_PATH = 'data/clean-users.json'
CLEAN_SESSIONS_PATH = 'data/clean-sessions.json'
CLEAN_PRODUCTS_PATH = 'data/clean-products.json'


def create_model_input(users, sessions, products):
    users = pd.DataFrame(users)
    sessions = pd.DataFrame(sessions)
    products = pd.DataFrame(products)

    merged = sessions.merge(products, on='product_id')
    merged_cleaned = merged.drop(columns=['purchase_id', 'product_name', 'offered_discount'])
    return merged_cleaned.to_dict(orient='records')
