import allure
import pytest
import logging


@allure.title('日流向上传功能校验')
@pytest.mark.init
def st11a1rt(instance, excel, case_path_manage):
    flow_template_path = case_path_manage("day_flow_template.xlsx")
    test_data_res_path = case_path_manage("day_flow_template_res.xlsx")

    flow_template_stream = instance.sfe.get_day_flow_template()
    flow_template_path.write_bytes(flow_template_stream.content)

    excel.load(flow_template_path)
    logging.info(excel.columns)

    test_df = excel.create_test_data(10)
    excel.to_excel(test_data_res_path, test_df)
    print(test_data_res_path)
    # assert ...
