from basic.http_client import BasicHttpClient
from basic.Environment import Environment
import allure


class CrmManage(BasicHttpClient):

    def __init__(self):
        super().__init__(**Environment().environment_dict)

    @allure.step('获取拜访场景')
    def get_call_template_list(self, user_id=None, call_data=None):
        path = r'/gw/api/call-api-svc/api/call/template/list'
        payload = {
            'userId': user_id,
            'date': call_data
        }

        return self._request('post', path, json=payload)

    @allure.step('获取拜访机构列表')
    def get_call_institution_list(self, user_id=None, institution_type='HOSPITAL', ):
        path = f'/gw/api/crm-jurisdiction-api-svc/api/institution/page/list'
        payload = {
            'institutionType': institution_type,
            'userId': user_id,
            'page': 1,
            'size': 20
        }

        return self._request('post', path, json=payload)

    @allure.step('获取客户列表')
    def get_customer_by_institution(self, institution_id=None, user_id=None):
        path = '/gw/api/crm-jurisdiction-api-svc/api/customer/page/list'

        payload = {
            "onlyTargetDoctor": False,
            "institutionId": institution_id,
            "userId": user_id,
            "customerType": "DOCTOR",
            "page": 1,
            "size": 5
        }

        return self._request('post', path, json=payload)
