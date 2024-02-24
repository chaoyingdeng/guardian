import pandas as pd
from pathlib import Path


def check_columns_contains(file_path, columns_name):
    df = pd.read_excel(file_path)
    return columns_name in df.columns


class Excel:
    def __init__(self, excel_path: [Path, str]):
        self.excel_path = excel_path

    def open(self):
        return pd.read_excel(self)

