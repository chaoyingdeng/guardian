from basic.http_client import BasicHttpClient
from basic.Environment import Environment


class SassManage(BasicHttpClient):
    pass


def connect():
    return SassManage(*Environment.get())
