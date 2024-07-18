import allure
import pytest


@allure.title('月流向数据上传流程校验')
@pytest.mark.init
def start(instance, excel, case_path_manage):
    flow_template_path = case_path_manage('month_flow_template.xlsx')
    test_data_res_path = case_path_manage('month_flow_template_res.xlsx')

    flow_template_stream = instance.sfe.get_day_month_template()
    flow_template_path.write_bytes(flow_template_stream.content)

    excel.load(flow_template_path).create_test_data()
    excel.to_excel(test_data_res_path)

    pre_period = instance.sfe.get_pre_period().get('id')

    import_resp = instance.sfe.month_flow_import(test_data_res_path, pre_period)
    file_token = import_resp.get('token')
    resp = instance.sfe.month_flow_commit(period_id=pre_period, file_token=file_token)

    assert resp, '月流向上传失败'
