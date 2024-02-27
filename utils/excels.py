import random

import pandas as pd
from basic.exceptions import ColumnNotExistsError
from utils.decorator import Decorator
from utils.data_pool import DataPool
from utils.times import Times


def check_columns_contains(file_path, columns_name):
    df = pd.read_excel(file_path)
    return columns_name in df.columns


class Excel:
    def __init__(self, excel_path=None):
        self._df = None
        self._columns = None
        self.row_size = 10
        self.columns_size = None
        self._load = False
        self.data_poll = DataPool()
        self.today = Times().today
        if excel_path:
            self.load(excel_path)

    @property
    def columns(self):
        return self._columns

    def load(self, excel_path):
        self._df = self._open(excel_path)
        self._columns = self._df.columns
        self.row_size, self.columns_size = self._df.shape
        self._load = True
        return self

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

    def write_data_(self, column, value):
        self._df[column] = value

    @Decorator.check_load
    def to_excel(self, file_path):
        return self._df.to_excel(file_path, index=False)

    def create_test_data(self, target_columns: [], size):
        for _ in target_columns:
            for column in target_columns:
                cc = []
                line_data = self.guess_column_type(column)
                cc.append(line_data)
            res = []
            res.append(list(_).append(cc))
        return res

    def guess_column_type(self, column_name):
        if '日期' in column_name:
            return self.today
        elif '机构编码' in column_name or '经销商编码' in column_name or '客户编码' in column_name:
            return self.data_poll.institution.code
        elif '机构名称' in column_name or '经销商名称' in column_name or '客户名称' in column_name:
            return self.data_poll.institution.get_name(self.data_poll.institution.code)
        elif '产品编码' in column_name:
            return self.data_poll.product.code
        elif '产品名称' in column_name:
            return self.data_poll.product.get_name(self.data_poll.product.code)
        elif '数量' in column_name:
            return random.randint(100, 200)
        else:
            return self.data_poll.product.code


if __name__ == '__main__':
    from pathlib import Path

    p = Path(__file__).parent.parent / 'data' / 'test_upload_day_flow' / 'day_flow_template.xlsx'
    excel = Excel()
    print(excel.load(p)._df)
    res = excel.create_test_data(
        ['*销售日期', '*经销商编码', '*经销商名称', '*客户编码', '*客户名称', '*产品编码', '*产品名称', '*产品规格',
         '*数量', '*单位'], 2)
    print(res)
    for i in range(len(res[0])):
        excel.write_data_(res[0][i], res[1][i])
        excel.write_data_(res[0][i], res[2][i])
    print(excel.load(p)._df)
