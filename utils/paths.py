from pathlib import Path


class Paths:
    def __init__(self):
        self._project_path = Path(__file__).absolute().parent.parent
        self._data_path = self._project_path / 'data'

    @property
    def project_path(self):
        return self._project_path

    def create_case_test_file_path(self, case_name, file_name) -> Path:
        """ 根据传入的用例名称和文件名新建文件并返回文件路径 """
        dir_paths = self._data_path.joinpath(case_name)
        dir_paths.mkdir(exist_ok=True)

        file_path = (dir_paths.joinpath(file_name))
        file_path.touch(exist_ok=True)
        return file_path


if __name__ == '__main__':
    p = Paths()
    s = '123'
    print(p.create_case_test_file_path('123', '5.txt'))
    print(type(p.create_case_test_file_path('123', '5.txt')))
