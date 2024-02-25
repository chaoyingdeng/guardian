import allure
import copy
from basic.http_client import BasicHttpClient
from basic.Environment import Environment
from pathlib import Path


class SfeManage(BasicHttpClient):

    def __init__(self):
        super().__init__(**Environment().environment_dict)

    @allure.step('月流向列表查询')
    def month_flow_query(self, period_id, data_version):
        path = '/gw/api/sales-operation-sfe-admin-svc/flow/month/list'
        payload = {
            'query': {
                'periodId': period_id,
                'dataVersion': data_version
            }
        }
        return self._request('post', path, json=payload)

    @allure.step('流向明细查询')
    def month_flow_detail(self, flow_id):
        path = f'/gw/api/sales-operation-sfe-admin-svc/flow/month/detail/{flow_id}'
        return self._request('get', url=path)

    @allure.step('月销量查询')
    def month_sales_query(self, period_id, sale_type, user_id):
        path = '/gw/api/data-hub-api-route-svc/data-api/proxy/sfe/saleMonthSum'
        payload = {
            'periodId': period_id,
            'saleDataType': sale_type,
            'userId': user_id,
            'pageNo': 1,
            'pageSize': 10,
            'current': 1
        }
        return self._request('get', path, params=payload)

    @allure.step('获取上个账期')
    def get_pre_period(self):
        path = '/gw/api/sales-operation-sfe-admin-svc/period/getPreviousPeriodByDate'

        return self._request('get', path)

    @allure.step('获取日流向模板')
    def get_day_flow_template(self):
        path = '/gw/api/sales-operation-sfe-admin-svc/flow/day/template/download'
        return self._request('get', path)

    @allure.step('上传日流向')
    def day_flow_import(self, file_path):
        path = '/gw/api/sales-operation-sfe-admin-svc/flow/day/import'
        headers = copy.deepcopy(self._headers)
        headers.pop('Content-Type')
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f)}
            resp = self._request('post', path, headers=headers, files=files)
        return resp

    @allure.step('提交日流向')
    def day_flow_commit(self, file_token):
        path = '/gw/api/sales-operation-sfe-admin-svc/flow/day/import/commit'
        payload = {
            "success": True,
            "token": file_token,
            "fileName": None,
            "requestUrl": "/download/error?errorToken=null",
            "dataToken": file_token,
            "dataConvertToken": None,
            "errorToken": None
        }
        return self._request('post', path, json=payload)

    @allure.step('日月流向任务列表查询')
    def flow_task_query(self, collect_mob=None, collect_type=None, create_name=None, date_begin=None, date_end=None):
        path = '/gw/api/sales-operation-sfe-admin-svc/flow/filetask/list'
        payload = {
            "query": {
                "collectMob": collect_mob,
                "collectType": collect_type,
                "createByName": create_name,
                "dateBegin": date_begin,
                "dateEnd": date_end
            },
            "sorter": {"orders": [{"direction": "desc", "property": "createTime"}]}
        }
        return self._request('post', path, json=payload)

    # --------------#
    # 指标相关       #
    # --------------#
    @allure.step('获取财年列表')
    def get_financial_year__list(self):
        path = '/gw/api/indicator-admin-svc/admin/indicator/financial/list'
        return self._request('get', path)

    @allure.step('校验对应财年指标配置是否存在')
    def get_indicator_config(self, year_id):
        path = f'/gw/api/indicator-admin-svc/admin/indicator/config/{year_id}'
        return self._request('get', path)

    @allure.step('指标列表查询')
    def get_indicator_list(self, year_id, indicator_type=None, node_list=None):
        path = '/gw/api/indicator-admin-svc/admin/indicator/page?current=1&size=20'
        payload = {
            "financialYearId": year_id,
            "isTarget": indicator_type,
            "nodeCodeList": [node_list]
        }
        return self._request('post', path, json=payload)

    @allure.step('获取账期列表')
    def get_indicator_period_list(self, year_id):
        path = f'/gw/api/indicator-admin-svc/admin/indicator/period/list/{year_id}'
        return self._request('get', path)

    @allure.step('导出指标模板')
    def export_indicator_template(self, period_list: []):
        path = '/gw/api/indicator-admin-svc/admin/indicator/template/export'
        payload = {
            "financialYearId": "8ac276a18c1542e7018ce7207d060031",
            "periodIdList": period_list
        }
        return self._request('post', path, json=payload)
