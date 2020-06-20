from embeddings.vectorization import Vectorizer
from preprocessing.data_cleaner import DataCleaner
from utils.files_io import load_jsonl, write_json_file

from preprocessing.merger import Merger
from sklearn.model_selection import train_test_split

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
        self.merger = Merger()

    def preprocess_data(self, raw_users, raw_sessions, raw_products):
        clean_users, clean_sessions, clean_products = self.data_cleaner.clear_data(raw_users, raw_sessions,
                                                                                   raw_products)
        write_data(self.save_dir, clean_users, clean_sessions, clean_products)
        clean_products = self.vectorizer.prepare_products(clean_products)
        merged_data = self.merger.create_model_input(clean_sessions, clean_products)

        x, y = self.merger.split_into_x_y(merged_data)
        x = self.merger.represent_session_as_single_row(x, y, clean_products)
        y = self.merger.represent_bought_products_as_matrix(y, clean_products)

        return x, y

    def save_train_test_split(self, x, y, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)
        write_json_file(self.save_dir + 'X_train.json', X_train)
        write_json_file(self.save_dir + 'y_train.json', y_train)
        write_json_file(self.save_dir + 'X_test.json', X_test)
        write_json_file(self.save_dir + 'y_test.json', y_test)


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
    x, y = preprocessor.preprocess_data(users, sessions, products)
    preprocessor.save_train_test_split(x, y)


if __name__ == '__main__':
    main()
