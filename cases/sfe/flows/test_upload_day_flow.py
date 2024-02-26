import allure
import pytest
from utils.decorator import Decorator


@allure.title('日流向上传功能校验')
@pytest.mark.init
@Decorator.handle_guardian_error
def start(instance, case_path_manage, excel, faker):
    flow_template_stream = instance.sfe.get_day_flow_template()
    p = case_path_manage('day_flow_template.xlsx')
    with open(p, 'wb') as file:
        file.write(flow_template_stream.content)

    excel.load(p)
    assert excel.check_columns_contains('流向ID')
    assert excel.check_columns_contains('*销售日期')

    flow_res = case_path_manage('day_flow_template_res.xlsx')
    excel.write_data('销售日期', faker.random_int)
    excel.to_excel(flow_res)
