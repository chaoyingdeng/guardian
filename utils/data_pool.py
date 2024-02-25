from abc import ABC, abstractmethod
import numpy as np


class DataPool(object):
    def __init__(self):
        self._product = Product()
        self._institution = Institution()
        self._doctor = Doctor()

    @property
    def product(self):
        return self._product

    @property
    def institution(self):
        return self._institution

    @property
    def doctor(self):
        return self._doctor


class AbstractTestData(ABC):
    def __init__(self):
        self.size = 50  # 这里设置了一个默认值
        self._info = self.load()
        self.codes = list(self._info.keys())
        self.names = list(self._info.values())

    @abstractmethod
    def load(self):
        pass

    def get_code(self, size=1):
        return np.random.choice(self.codes, max(1, size))

    def get_name(self, code=None):
        return np.random.choice(self.names) if not code else self._info.get(code, None)


class Institution(AbstractTestData):
    def load(self):
        return {f'H{10000 + index}': f'{index}号机构' for index in range(self.size)}


class Product(AbstractTestData):

    def load(self):
        return {f'P{20000 + index}': f'{20000 + index}号产品' for index in range(self.size)}


class Doctor(AbstractTestData):

    def load(self):
        return {f'D{30000 + index}': f'{30000 + index}号医生' for index in range(self.size)}


if __name__ == '__main__':
    d = DataPool()
    print(d.doctor.get_code(900))  # 输出为 60
