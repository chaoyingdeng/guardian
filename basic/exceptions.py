class GuardianError(Exception):
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
