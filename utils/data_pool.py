from utils.fakes import Fakers
import random

faker = Fakers()


class DataPool:
    pass


class Institution:
    def __init__(self):
        self.info = {}
        self.size = 50
        self.load()

    def load(self):
        for _ in range(self.size):
            self.info.setdefault(f'H{random.randint(10000000, 99999999)}', *faker.get_hospital_name())


class Product:
    _product = [
        '感康', '美平', '白蛋白', '叶绿素', '布洛芬', '青青草', '止咳糖浆',
    ]

    def __init__(self):
        self.size = 7
        self.info = {}
        self.load()

    def load(self):
        for _ in range(self.size):
            self.info.setdefault(f'P{random.randint(10000000, 99999999)}', self._product[_])


if __name__ == '__main__':
    prod = Product()
    print(prod.info)
