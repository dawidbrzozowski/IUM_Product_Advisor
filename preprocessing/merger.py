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
    merged_cleaned = merged.drop(columns=['purchase_id', 'product_name', 'offered_discount', 'user_id'])
    merged_cleaned.sort_values(by=['session_id'], inplace=True)
    return merged_cleaned.to_dict(orient='records')


def split_into_x_y(merged_data):
    print(type(merged_data))

    x = []
    y = []
    for row in merged_data:
        if row['event_type'] == 'BUY_PRODUCT':
            y.append({'session_id': row['session_id'], 'product_id': row['product_id']})
        else:
            row.pop('event_type')
            x.append(row)

    # drop session that had no buy event
    print(len(y))
    print(len(x))

    return x, y
