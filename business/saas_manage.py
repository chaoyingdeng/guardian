from basic.http_client import BasicHttpClient
from basic.Environment import Environment


class SassManage(BasicHttpClient):
    def __init__(self):
        super().__init__(**Environment().environment_dict)





