import allure


@allure.title('修改FAQ热点状态')
def start(instance):
    category_list = instance.cms.get_category_list('FAQ')
    root_category = category_list.get('id')

    faq = instance.cms.get_faq_list(root_category)
    modify_faq_id = faq.get('records')[0].get('id')
    current_status = faq.get('records')[0].get('heat')

    resp = instance.cms.modify_faq_heat(faq_id=modify_faq_id, is_heat=not current_status)
    assert resp, 'modify Fail'
