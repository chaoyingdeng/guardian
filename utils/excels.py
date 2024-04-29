import pandas as pd
from basic.exceptions import ColumnNotExistsError
from basic.exceptions import ExcelConvertError
from utils.data_pool import guess_column
from pathlib import Path
import warnings
import logging

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.*")


class Excel:
    def __init__(self, excel_path=None):
        self._df = pd.DataFrame()
        if excel_path:
            self.load(excel_path)

    @property
    def columns(self):
        print(self._df.columns)
        return self._df.columns

    @property
    def rows(self):
        logging.info(f'数据详情 = {self._df.info}')
        return self._df.shape[0]

    @property
    def target_columns(self):
        res = []
        for column in self.columns:
            match str(column):
                case c if c.startswith('*'):
                    res.append(c)
                case c if any(c == keyword for keyword in ['机构编码', '产品编码']):
                    res.append(c)
                case c if any(keyword in c for keyword in ['规格', '考核价', '父级产品编码', '单位']):
                    res.append(c)
        return res

    def load(self, path: Path | str, header=0):
        self._df = pd.read_csv(path, header=header) if str(path).endswith('.csv') else pd.read_excel(path,
                                                                                                     header=header)
        logging.info(f'{path.name} 成功加载, 字段名 = {self._df.columns}')
        return self

    def write_column(self, column, fn):
        if column not in self._df.columns:
            raise ColumnNotExistsError(column)

        for i in range(len(self._df)):
            self._df.at[i, column] = fn()

        return self

    def to_excel(self, file_path: str | Path, ):
        try:
            logging.info(f'writer test data to {file_path}')
            self._df.to_excel(file_path, index=False)
        except Exception as e:
            raise ExcelConvertError(e)

    def create_test_data(self, size=1):
        for column in self.target_columns:
            self._df[column] = guess_column(column, size)

        return self._df
