import random
from abc import ABC, abstractmethod
from collections import namedtuple
from uuid import uuid4

from utils.decorator import Decorator
from utils.fakes import Fakers
from utils.times import Times

faker = Fakers()
SIZE = 10


def _uuid():
    return str(uuid4()).replace('-', '')


@Decorator.singleton
class DataPool:
    def __init__(self):
        self.institution = Institutions()
        self.product = Products()


class AbstractTestData(ABC):
    def __init__(self):
        self.size = SIZE
        self.info = self.load()

    @abstractmethod
    def load(self):
        pass

    @property
    def codes(self):
        return [_item.code for _item in self.info][:SIZE]

    @property
    def names(self):
        return [_item.name for _item in self.info][:SIZE]

    def locator(self, value_name):
        return [getattr(item, value_name, None) for item in self.info][:SIZE]


class Institutions(AbstractTestData):
    def load(self):
        # 创建 Institution 命名元组类型
        Institution = namedtuple('Institution', ['code', 'name', 'province', 'city', 'county', 'status'])
        return [Institution(_uuid(), faker.get_hospital_name(), '甘肃省', '平凉市', '静宁县', 'active') for _ in
                range(self.size)]


class Products(AbstractTestData):
    def load(self):
        Product = namedtuple('Product', ['code', 'name', 'level', 'unit', 'spec', 'price', 'status'])
        return [Product(_uuid(), faker.get_product_name(), 'sku', '盒', '30mg', 11.5, 'active') for _ in
                range(self.size)]


def guess_column(column: str, size):
    """ 使用模式匹配处理 """
    _size = min(SIZE, size)
    data_pool = DataPool()
    match column:
        case col if '日期' in col:
            return [Times().today for _ in range(_size)]
        case col if '月' in col:
            return [Times().period for _ in range(_size)]
        case col if 'ID' in col.upper():
            return [_uuid() for _ in range(_size)]
        case col if '金额' in col or '值' in col:
            return [round(random.uniform(1, 100), 2) for _ in range(_size)]
        case col if '数量' in col:
            return [random.randint(1, 100) for _ in range(_size)]
        case col if '编码' in col and ('经销商' in col or '客户' in col or '机构' in col):
            return data_pool.institution.locator('code')
        case col if '编码' in col and '品' in col:
            return data_pool.product.locator('code')
        case col if '名称' in col and ('经销商' in col or '客户' in col or '机构' in col):
            return data_pool.institution.locator('name')
        case col if '名称' in col and '品' in col:
            return data_pool.product.locator('name')
        case col if '单位' in col:
            return data_pool.product.locator('unit')
        case col if '规' in col:
            return data_pool.product.locator('spec')
        case col if '考核价' in col:
            return data_pool.product.locator('price')
        case col if '产品层级' in col:
            return data_pool.product.locator('level')
        case _:
            return '测试数据填充'
