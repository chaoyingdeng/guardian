from basic.http_client import BasicHttpClient
from basic.Environment import Environment
import allure


class SassManage(BasicHttpClient):
    def __init__(self):
        super().__init__(**Environment().environment_dict)

    @allure.step('获取字典详情')
    def get_dict_detail_by_id(self, dict_id):
        path = f'/gw/api/paas-extmodel-svc/dictionary/listByIds'

        payload = [dict_id]

        return self._request('post', path, json=payload)
