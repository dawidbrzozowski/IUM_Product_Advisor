from embeddings.vectorization import Vectorizer
from preprocessing.data_cleaner import DataCleaner
from utils.files_io import load_jsonl, write_json_file

from preprocessing.merger import create_model_input, split_into_x_y, represent_session_as_single_row

DEFAULT_USERS_PATH = 'data/unprocessed/users.jsonl'
DEFAULT_SESSIONS_PATH = 'data/unprocessed/sessions.jsonl'
DEFAULT_PRODUCTS_PATH = 'data/unprocessed/products.jsonl'


class Preprocessor:
    def preprocess_data(self, raw_users, raw_sessions, raw_products):
        pass


class BaselinePreprocessor(Preprocessor):
    def __init__(self):
        self.save_dir = 'data/baseline/'
        self.data_cleaner = DataCleaner()

    def preprocess_data(self, raw_users, raw_sessions, raw_products):
        return self.data_cleaner.clear_data(raw_users, raw_sessions, raw_products)


class NeuralNetworkPreprocessor(Preprocessor):
    def __init__(self):
        self.save_dir = 'data/neural_network/'
        self.data_cleaner = DataCleaner()
        self.vectorizer = Vectorizer()

    def preprocess_data(self, raw_users, raw_sessions, raw_products):
        clean_users, clean_sessions, clean_products = self.data_cleaner.clear_data(raw_users, raw_sessions,
                                                                                   raw_products)
        clean_products = self.vectorizer.prepare_products(clean_products)
        return clean_users, clean_sessions, clean_products


def read_data(users_path=DEFAULT_USERS_PATH, sessions_path=DEFAULT_SESSIONS_PATH,
              products_path=DEFAULT_PRODUCTS_PATH):
    users = load_jsonl(users_path)
    sessions = load_jsonl(sessions_path)
    products = load_jsonl(products_path)
    return users, sessions, products


def write_data(save_dir, clean_users, clean_sessions, clean_products):
    write_json_file(save_dir + 'clean-users', clean_users)
    write_json_file(save_dir + 'clean-sessions', clean_sessions)
    write_json_file(save_dir + 'clean-products', clean_products)


def main():
    users, sessions, products = read_data()
    preprocessor = NeuralNetworkPreprocessor()
    clean_users, clean_sessions, clean_products = preprocessor.preprocess_data(users, sessions, products)
    write_data(preprocessor.save_dir, clean_users, clean_sessions, clean_products)

    merged_data = create_model_input(clean_users, clean_sessions, clean_products)
    merged_data = represent_session_as_single_row(merged_data, clean_products)

    # write_json_file(preprocessor.save_dir + 'Y')
    x, y = split_into_x_y(merged_data)
    # print(x)

if __name__ == '__main__':
    main()
