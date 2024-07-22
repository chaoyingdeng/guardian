import datetime

import requests
import logging
from requests.adapters import HTTPAdapter
import setting


class BasicHttpClient:
    _session = requests.Session()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def __init__(self, env, tenant_id, account, password):
        self.env = env
        self.tenant_id = tenant_id
        self.account = account
        self.password = password
        self.base_path = f'https://{self.env}.pharmaos.com'
        self._headers = {}
        tenant_info = self.login_pharma()
        self.header('tm-header-token', tenant_info['bearerToken'])
        self.header('Content-Type', 'application/json;charset=utf-8', )
        self.header('tm-header-tenantid', tenant_info['tenantId'])
        self.header('tm-header-userid', tenant_info['userId'])
        cookie = "; ".join([f"{key}={value}" for key, value in self._session.cookies.items()])
        self.header('cookie', cookie)

    def header(self, name, value):
        self._headers[name] = value

    def login_pharma(self):
        account_json = {
            'account': self.account,
            'password': self.password
        }
        account_url = f'{self.base_path}/api/paas-user-web/login/account'
        account_details_url = f'{self.base_path}/api/paas-user-web/end-point?redirectURL={self.base_path}/gw/api/saas-web/cas-client/account-details?appCode=saas'
        account = f'{self.base_path}/gw/api/saas-web/cas-client/account-details?appCode=saas'
        cut_target_tenant = f'{self.base_path}/api/paas-user-web/account/tenant-default/{setting.account_id}/{self.tenant_id}'

        data = {
            'tenantId': self.tenant_id
        }

        self._session.request("POST", account_url, data=account_json)
        self._session.request("GET", account_details_url)
        self._session.request("PUT", cut_target_tenant, data=data)

        tenant_info = self._session.request("GET", account)
        resp = tenant_info.json().get('data')
        return resp

    def _request(self, method, url, headers=None, params=None, data=None, json=None, files=None):
        # 每个请求都使用新的session
        with requests.session() as session:
            # 设置请求失败重试
            session.mount("https://", HTTPAdapter(max_retries=3))
            return self._send(session, method, url, headers=headers, params=params, data=data, json=json, files=files)

    def _send(self, session, method, url, headers=None, params=None, data=None, json=None, files=None):
        """记录日志，并且赋予token"""
        if headers is None:
            headers = self._headers
        _url = self.base_path + url
        _resp = session.request(method, _url, headers=headers, params=params, data=data, json=json, files=files)
        logging.info(f'current_time = {datetime.datetime.now()}')
        logging.info(f'response time :{_resp.elapsed.total_seconds()}')
        logging.info(f'current api:{_resp.request.url},\njson: {_resp.request.body}\nresp: {_resp.text} \ndone\n\n')

        if _resp.headers.get('content-type', '').startswith('application/json'):
            json_resp = _resp.json()
            # 如果 'data' 字段不是 None
            if 'data' in json_resp and json_resp['data'] is not None:
                return json_resp['data']
            else:
                # 返回整个 JSON 响应
                return json_resp
        else:
            return _resp  # 如果不是 JSON 格式的数据，则返回原始响应文本
