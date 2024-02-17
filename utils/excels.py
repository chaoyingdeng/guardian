import pandas as pd


def check_columns_contains(file_path, columns_name):
    df = pd.read_excel(file_path)
    return columns_name in df.columns
