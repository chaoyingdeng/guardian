import time
import requests
import allure
import pytest
from utils.get_path import get_data_path
from utils.excels import check_columns_contains


@allure.title('日流向上传功能校验')
@pytest.mark.init
def start(instance):
    res = instance.sfe_manage.get_day_flow_template()
    if res.status_code == 200:
        p = get_data_path('test_upload_day_flow', 'day_flow_template.xlsx')
        with open(p, 'wb') as file:
            file.write(res.content)
    else:
        raise requests.HTTPError()

    assert check_columns_contains(p, '流向ID')
    assert check_columns_contains(p, '*销售日期')

    file_path = get_data_path('test_upload_day_flow', 'day_flow_template1.xlsx')
    res1 = instance.sfe_manage.day_flow_import(file_path)
    assert res1.json().get('data').get('success')

    time.sleep(1)
    file_token = res1.json().get('data').get('token')
    res2 = instance.sfe_manage.day_flow_commit(file_token)
    assert res2
