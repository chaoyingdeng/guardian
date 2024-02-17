import allure


@allure.title('指标列表查询功能校验')
def start(instance):
    year_id = instance.sfe_manage.get_financial_year__list().json().get('data')[0].get('id')

    resp = instance.sfe_manage.get_indicator_list(year_id)
    assert resp

