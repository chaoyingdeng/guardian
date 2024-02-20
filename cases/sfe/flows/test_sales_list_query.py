import allure


@allure.title('月流向列表查询功能校验')
def start(instance):
    pre_period = instance.sfe.get_pre_period().json().get('data').get('id')
    resp_1 = instance.sfe.month_flow_query(pre_period, 1)
    assert resp_1.json().get('data').get('pager').get('total'), f'month flows query failed{resp_1.json().get("msg")}'

    flow_id = resp_1.json().get('data').get('content')[0].get('id')
    resp_2 = instance.sfe.month_flow_detail(flow_id)
    assert resp_2.json().get('data').get('id') == flow_id
