import pandas as pd
from basic.exceptions import ColumnNotExistsError
from utils.data_pool import guess_column


class Excel:
    def __init__(self, excel_path=None):
        self._df = pd.DataFrame()
        if excel_path:
            self.load(excel_path)

    @property
    def columns(self):
        return self._df.columns

    def load(self, path):
        self._df = pd.read_csv(path) if str(path).endswith('.csv') else pd.read_excel(path)
        return self

    def write_column(self, column, fn):
        if column not in self._df.columns:
            raise ColumnNotExistsError(column)
        self._df[column] = [fn() for _ in range(len(self._df))]
        return self

    def to_excel(self, file_path, df=None):
        # 如果没有提供 DataFrame，就使用内部的 _df
        if df is None:
            df = self._df
        df.to_excel(file_path, index=False)

    def create_test_data(self, size=5):
        test_df = pd.DataFrame()
        for column in self._df.columns:
            test_df[column] = guess_column(column, size)
        return test_df
