from pathlib import Path


class Paths:
    def __init__(self):
        self._project_path = Path(__file__).absolute().parent.parent
        self._data_path = self._project_path / 'data'

    @property
    def project_path(self):
        return self._project_path

    def make_file(self, dir_path, file_name) -> Path:
        """ 根据传入的路径和文件名新增文件 """
        dir_path = self._data_path / dir_path.mkdir(exist_ok=True)
        res_path = dir_path / file_name
        res_path.touch(exist_ok=True)
        return res_path
