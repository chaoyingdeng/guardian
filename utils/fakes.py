from faker import Faker
import numpy as np

_hospital_name = [
    '协和医院',
    '人民医院',
    '中医院',
    '康复医院',
    '第一医院',
    '解放军医院',
    '玛丽医院',
    '东华医院',
    '仁济医院',
    '明爱医院',
    '眼科医院',
    '仁安医院',
    '第三医院',
    'xx附属医院',
]

_departments = [
    '内科', '中医科', '外科', '头颈科', '眼科', '儿科', '耳鼻喉科', '骨科',
]

_product = [
    '感康', '美平', '白蛋白', '叶绿素', '布洛芬', '青青草', '止咳糖浆',
]
faker = Faker(['zh_CN'])


def get_hospital_name():
    return faker.city() + np.random.choice(_hospital_name)


def get_doctor_name():
    return faker.name()


def get_department_name():
    return np.random.choice(_departments)


def get_product_name():
    return np.random.choice(_product)
