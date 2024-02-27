from utils.fakes import Fakers
import random
from abc import ABC, abstractmethod

faker = Fakers()


class DataPool:
    def __init__(self):
        self.institution = Institution()
        self.product = Product()


class AbstractTestData(ABC):
    def __init__(self):
        self.size = 10
        self.info = self.load()

    @abstractmethod
    def load(self):
        pass

    @property
    def codes(self):
        return list(self.info.keys())

    @property
    def names(self):
        return list(self.info.values())

    @property
    def code(self):
        return random.choice(self.codes)

    def get_name(self, code):
        return self.info.get(code)


class Institution(AbstractTestData):
    def load(self):
        return {f'H{10000 + index}': f'{10000 + index}号机构' for index in range(self.size)}


class Product(AbstractTestData):
    def load(self):
        return {f'P{20000 + index}': f'{20000 + index}号产品' for index in range(self.size)}




if __name__ == '__main__':
    prod = Product()
    print(prod.info)
    print(prod.get_name('P20000'))
