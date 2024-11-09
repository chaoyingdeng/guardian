from basic.http_client import BasicHttpClient
from basic.Environment import Environment
import allure


class CmsManage(BasicHttpClient):
    def __init__(self):
        super().__init__(**Environment().environment_dict)

    def get_tm_token(self):
        path = f'/gw/api/saas-web/open/get-tm-token'
        return self._request('GET', path)

    @allure.step('获取目录列表')
    def get_category_list(self, category_type):
        """ 获取目录列表 """
        path = r'/gw/api/cms-api-svc/admin/category/load'
        payload = {
            'categoryType': category_type
        }

        return self._request('GET', path, params=payload)

    @allure.step('目录操作')
    def category_handle(self, parent_id, category_name):
        """ 操作目录接口 """
        path = r'/gw/api/cms-api-svc/admin/category'
        payload = {
            "defaultValue": category_name,
            "name": category_name,
            "parentId": parent_id
        }

        return self._request('POST', path, json=payload)

    @allure.step('目录删除')
    def delete_category(self, category_id):
        """ 删除目录 """
        path = rf'/gw/api/cms-api-svc/admin/category/{category_id}'
        return self._request('DELETE', path)

    @allure.step('获取FAQ列表')
    def get_faq_list(self, category_id, key_word=None, is_heat=None):
        """ 获取FAQ列表 """
        path = r'/gw/api/cms-api-svc/admin/faq/page'
        payload = {
            "categoryId": category_id,
            "keywords": key_word,
            "heat": is_heat
        }

        return self._request('POST', path, json=payload)

    @allure.step('上传文件')
    def file_upload(self, tenant_id, file_path):
        """ 上传文件 """
        path = r'/file/upload?repositoryName=knowledge-base-pc'

        payload = {'needTransfer': 'false',
                   'processor': 'resources',
                   'appId': 'knowledge-base-pc',
                   'tenantId': tenant_id}

        files = [
            ('file', ('tree.jpg', open(file_path, 'rb'), 'image/jpeg'))
        ]

        user_token = self.get_tm_token().get('userToken')
        headers = {
            'Cookie': f'token={user_token}'
        }

        return self._request("POST", path, data=payload, files=files, headers=headers)

    @allure.step('新增FAQ')
    def add_faq(self, category_id, question_name, file_path):
        path = r'/gw/api/cms-api-svc/admin/faq/save'
        payload = {
            'question': question_name,
            'answer': f"<p>测试<img src={file_path} alt="" data-href="" style=""/></p>",
            'id': None,
            'categoryId': category_id
        }
        return self._request("POST", path, json=payload)

    @allure.step('编辑FAQ')
    def faq_handle(self, category_id, question_name, answer_content, file_path, question_id):
        path = r'/gw/api/cms-api-svc/admin/faq/save'
        payload = {
            'question': question_name,
            'answer': f"<p>{answer_content}<img src={file_path} alt="" data-href="" style=""/></p>",
            'id': question_id,
            'categoryId': category_id
        }
        return self._request("POST", path, json=payload)

    @allure.step('修改FAQ热点标记')
    def modify_faq_heat(self, faq_id, is_heat):
        path = r'/gw/api/cms-api-svc/admin/faq/heat'
        payload = {
            'faqId': faq_id,
            'heat': is_heat
        }

        return self._request("POST", path, json=payload)
