import pandas as pd

from utils.files_io import load_jsonl

USER_PATH = 'data/users.jsonl'


def main():
    users = load_jsonl(USER_PATH)
    users_df = pd.DataFrame(users)
    print(users_df)


if __name__ == '__main__':
    main()
