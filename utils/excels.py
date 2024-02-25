import pandas as pd
from basic.exceptions import ColumnNotExistsError
from utils.decorator import Decorator


def check_columns_contains(file_path, columns_name):
    df = pd.read_excel(file_path)
    return columns_name in df.columns


class Excel:
    def __init__(self, excel_path=None):
        self._df = None
        self._columns = None
        self.row_size = None
        self.columns_size = None
        self._load = False
        if excel_path:
            self.load(excel_path)

    def load(self, excel_path):
        self._df = self._open(excel_path)
        self._columns = self._df.columns
        self.row_size, self.columns_size = self._df.shape
        self._load = True

    def _open(self, excel_path):
        return pd.read_csv(excel_path) if str(excel_path).endswith('csv') else pd.read_excel(excel_path)

    @Decorator.check_load
    def check_columns_contains(self, column):
        return column in self._columns

    @Decorator.check_load
    def write_data(self, column, fn):
        if not self.check_columns_contains(column):
            raise ColumnNotExistsError(column)
        self.check_columns_contains(column)
        self._df[column] = fn(self.row_size)
        return self

    @Decorator.check_load
    def to_excel(self, file_path):
        return self._df.to_excel(file_path, index=False)

    def guess_data(self):
        res = [column for column in self._columns if '*' in column]
