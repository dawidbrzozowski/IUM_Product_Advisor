import pandas as pd
from utils.files_io import write_json_file


def create_model_input(users, sessions, products):
    users = pd.DataFrame(users)
    sessions = pd.DataFrame(sessions)
    products = pd.DataFrame(products)

    merged = sessions.merge(products, on='product_id')
    merged_cleaned = merged.drop(columns=['purchase_id', 'product_name', 'offered_discount'])
    return merged_cleaned.to_dict(orient='records')


def represent_session_as_single_row(merged_data, clean_products):
    base_len = len(merged_data[0])
    product_ids = [product['product_id'] for product in clean_products]
    product_representation = {product_id: 0 for product_id in product_ids}

    averaged_sessions = []
    current_session_id = -1
    current_session_avg = None

    for single_session in merged_data:
        if single_session['session_id'] != current_session_id:
            print('zmiana')

            if current_session_id != -1:
                averaged_sessions.append(current_session_avg)

            current_session_id = single_session['session_id']
            current_session_avg = single_session
            current_session_avg.update(product_representation)

        product_id = single_session['product_id']
        current_session_avg[product_id] += 1


    print(averaged_sessions)
    return averaged_sessions


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
