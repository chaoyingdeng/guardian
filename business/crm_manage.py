from basic.http_client import BasicHttpClient
from basic.Environment import Environment
import allure
import setting


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

    @allure.step('获取拜访场景配置')
    def get_call_template_detail(self, template_id=None):
        path = r'/gw/api/call-api-svc/api/call/template/detail'
        payload = {
            'id': template_id
        }

        return self._request('get', path, params=payload)

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

    @allure.step('获取已有拜访用户')
    def get_called_customer_list(self, institution_id=None, call_date=None ):
        path = '/gw/api/call-api-svc/api/called/institution/customer/list'
        payload = {
            "institutionId": institution_id,
            "institutionType": "HOSPITAL",
            "customerType": "DOCTOR",
            "date": call_date,
            "userId": setting.user_id
        }
        return self._request('post', path, json=payload)

    @allure.step('创建2.0拜访计划')
    def create_call_plan(self, customer_id=None, template_id=None, institution_id=None, call_type=None,
                         call_purpose=None, call_date=None):
        path = '/gw/api/call-api-svc/api/call/create'

        payload = {
            "customers": [
                {
                    "customerId": customer_id
                }
            ],
            "date": call_date,
            "institutionId": institution_id,
            "purposeCodes": [
                call_purpose
            ],
            "callTypeCode": call_type,
            "templateId": template_id
        }

        return self._request('post', path, json=payload)
