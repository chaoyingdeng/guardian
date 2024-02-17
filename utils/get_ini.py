import configparser
from pathlib import Path


def read_config():
    cfg = configparser.ConfigParser()
    # 使用__file__来保证正确获取路径
    file_path = Path(__file__).absolute().parent.parent / 'pytest.ini'
    cfg.read(file_path, encoding='utf-8')
    return cfg


def get_ini(option_name, convert=None, default=None):
    """
    获取pytest.ini参数
    :param option_name:
    :param convert:
    :param default:
    :param file_path:
    :return:
    """
    cfg = read_config()

    option_value = cfg.get('pytest', option_name, fallback=None)

    if option_value is not None and convert:
        return convert(option_value)
    elif option_value is not None:
        return option_value
    else:
        return default
