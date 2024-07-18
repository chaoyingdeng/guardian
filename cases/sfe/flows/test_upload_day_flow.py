import allure
import pytest


@allure.title('日流向上传流程校验')
@pytest.mark.init
def start(instance, excel, case_path_manage):
    flow_template_path = case_path_manage("day_flow_template.xlsx")
    test_data_res_path = case_path_manage("day_flow_template_res.xlsx")

    flow_template_stream = instance.sfe.get_day_flow_template()
    flow_template_path.write_bytes(flow_template_stream.content)

    excel.load(flow_template_path).create_test_data()
    excel.to_excel(test_data_res_path)

    import_resp = instance.sfe.day_flow_import(test_data_res_path)
    file_token = import_resp.get('token')

    resp = instance.sfe.day_flow_commit(file_token)
    assert resp, '日流向上传失败'
