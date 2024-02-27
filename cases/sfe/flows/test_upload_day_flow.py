import time
import requests
import allure
import pytest
from utils.excels import check_columns_contains


@allure.title('日流向上传功能校验')
@pytest.mark.init
def start(instance, case_path_manage, excel):
    flow_template_stream = instance.sfe.get_day_flow_template()
    flow_template = case_path_manage('day_flow_template.xlsx')
    with open(flow_template, 'wb') as file:
        file.write(flow_template_stream.content)
    print(excel.load(flow_template).columns)
    target_columns = [column for column in excel.load(flow_template).columns if f'*' in column]
    print(target_columns)
    assert 1
