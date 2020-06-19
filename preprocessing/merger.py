import pandas as pd
from utils.files_io import write_json_file

def create_model_input(users, sessions, products):
    users = pd.DataFrame(users)
    sessions = pd.DataFrame(sessions)
    products = pd.DataFrame(products)

    merged = sessions.merge(products, on='product_id')
    merged_cleaned = merged.drop(columns=['purchase_id', 'product_name', 'offered_discount'])
    return merged_cleaned.to_dict(orient='records')

def split_into_x_y(merged_data):
    X = []
    Y = []
    for row in merged_data:
        if row['event_type'] == 'BUY_PRODUCT':
            Y.append({'session_id': row['session_id'], 'product_id': row['product_id']})
        else:
            row.pop('event_type')
            X.append(row)
    return get_matching_x_y(X, Y)


def get_matching_x_y(X, Y):
    y_sessions = set()
    for y in Y:
        y_sessions.add(y['session_id'])
    X_match = []
    for x in X:
        if x['session_id'] in y_sessions:
            X_match.append(x)
    return X_match, Y

