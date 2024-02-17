from pathlib import Path


def get_project_path():
    return Path(__file__).absolute().parent.parent


def get_data_path(base_path, file_name):
    base_url = get_project_path() / 'data' / base_path
    base_url.mkdir(parents=True, exist_ok=True)
    res = base_url / file_name
    res.touch(exist_ok=True)
    return res
