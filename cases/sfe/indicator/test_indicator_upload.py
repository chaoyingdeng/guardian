import allure


@allure.title('指标模板下载流程校验')
def start(instance, case_path_manage, excel):
    year_id = instance.sfe.get_financial_year_list()[-1].get('id')
    period_list = instance.sfe.get_indicator_period_list(year_id)
    period_id1 = period_list[0].get('periodId')
    period_id2 = period_list[1].get('periodId')
    res = instance.sfe.export_indicator_template(year_id, [period_id1, period_id2])

    indicator_temp_path = case_path_manage('indicator_template.xlsx')

    indicator_temp_path.write_bytes(res.content)
    excel.load(indicator_temp_path)
    assert excel.rows > 1
