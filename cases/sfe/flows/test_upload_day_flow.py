import time
import requests
import allure
import pytest
from utils.excels import check_columns_contains
from utils.paths import Paths


@allure.title('日流向上传功能校验')
@pytest.mark.init
def start(instance, case_path_manage, case_file_name):
    res = instance.sfe.get_day_flow_template()
    if res.status_code == 200:
        p = case_path_manage.create_case_test_file_path(case_file_name, 'day_flow_template.xlsx')
        with open(p, 'wb') as file:
            file.write(res.content)
    else:
        raise requests.HTTPError()

    assert check_columns_contains(p, '流向ID')
    assert check_columns_contains(p, '*销售日期')

    file_path = case_path_manage.create_case_test_file_path(case_file_name, "day_flow_template1.xlsx")
    res1 = instance.sfe.day_flow_import(file_path)
    assert res1.json().get('data').get('success')

    time.sleep(1)
    file_token = res1.json().get('data').get('token')
    res2 = instance.sfe.day_flow_commit(file_token)
    assert res2
