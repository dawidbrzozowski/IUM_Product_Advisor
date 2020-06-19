from embeddings.vectorization import Vectorizer
from preprocessing.data_cleaner import DataCleaner
from utils.files_io import load_jsonl, write_json_file

from preprocessing.merger import create_model_input
import pandas as pd

from preprocessing.timestamp_handler import TimestampHandler
from preprocessing.user_id_filler import UserIdFiller

SAVE_DIR = 'data/'
DEFAULT_USERS_PATH = SAVE_DIR + 'users.jsonl'
DEFAULT_SESSIONS_PATH = SAVE_DIR + 'sessions.jsonl'
DEFAULT_PRODUCTS_PATH = SAVE_DIR + 'products.jsonl'


class Preprocessor:

    def __init__(self):
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


def write_data(clean_users, clean_sessions, clean_products):
    write_json_file(SAVE_DIR + 'clean-users', clean_users)
    write_json_file(SAVE_DIR + 'clean-sessions', clean_sessions)
    write_json_file(SAVE_DIR + 'clean-products', clean_products)


def main():
    users, sessions, products = read_data()
    preprocessor = Preprocessor()
    clean_users, clean_sessions, clean_products = preprocessor.preprocess_data(users, sessions, products)
    write_data(clean_users, clean_sessions, clean_products)

    merged_data = create_model_input(clean_users, clean_sessions, clean_products)




if __name__ == '__main__':
    main()
