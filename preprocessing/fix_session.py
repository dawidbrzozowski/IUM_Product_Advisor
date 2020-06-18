from utils.files_io import load_json, write_json_file

if __name__ == '__main__':
    products = load_json('data/clean-products.json')
    product_ids = set()
    for product in products:
        product_ids.add(product['product_id'])
    sessions = load_json('data/clean-sessions.json')
    filtered_sessions = [session for session in sessions if session['product_id'] in product_ids]
    write_json_file('data/clean-sessions.json', filtered_sessions)
