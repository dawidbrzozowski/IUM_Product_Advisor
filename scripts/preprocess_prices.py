import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from utils.files_io import load_jsonl

PRODUCTS_PATH = '../data/products.jsonl'

def cut_off_rows_with_forbidden_values(frame, coulmn_name, bottom_boundary, top_boundary):
    frame = frame[(frame[coulmn_name] > bottom_boundary)]
    frame = frame[(frame[coulmn_name] <= top_boundary)]

def print_price_extremes(frame, coulmn_name, print_depth):
    frame.sort_values(coulmn_name, inplace=True, ascending=False)
    print(frame.head(print_depth))
    frame.sort_values(coulmn_name, inplace=True, ascending=True)
    print(frame.head(print_depth))

products = pd.DataFrame(load_jsonl(PRODUCTS_PATH))

column_name_with_forbidden_values = 'price'
price_bottom_boundary = 0
price_top_boundary = 10000
print_depth = 10

cut_off_rows_with_forbidden_values(products, column_name_with_forbidden_values, price_bottom_boundary, price_top_boundary)
print_price_extremes(products, column_name_with_forbidden_values,print_depth)
