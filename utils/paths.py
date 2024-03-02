from pathlib import Path

_PROJECT_ROOT: Path = Path(__file__).parent.parent


def project_path() -> Path:
    return _PROJECT_ROOT


def create_case_test_file_path(case_name: str, file_name: str) -> Path:
    """ 根据传入的用例名称和文件名新建文件并返回文件路径 """
    dir_paths = _PROJECT_ROOT.joinpath('data', case_name)
    dir_paths.mkdir(exist_ok=True)

    file_path = dir_paths.joinpath(file_name)
    file_path.touch(exist_ok=True)
    return file_path
