class GuardianError(AttributeError):
    def __str__(self):
        return 'Guardian Error'


class EmailSendError(GuardianError):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return f'Email Send Fail: {self._msg}'


class FileNotExistError(GuardianError):
    def __init__(self, file_path):
        self._file_path = file_path

    def __str__(self):
        return f'File Not Exists: {self._file_path}'


class FileHandleError(GuardianError):
    def __init__(self, file_path):
        self._file_path = file_path

    def __str__(self):
        return f'File Handle Fail: {self._file_path}'


class ColumnNotExistsError(GuardianError):
    def __init__(self, column):
        self._column = column

    def __str__(self):
        return f'Column Not Exists: {self._column}'


class ExcelNotLoadError(GuardianError):
    def __str__(self):
        return f'Excel Not Load'
