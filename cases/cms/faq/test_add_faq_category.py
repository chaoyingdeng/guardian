import allure


@allure.title('新增FAQ目录')
def start(instance):
    category_list = instance.cms.get_category_list('FAQ')
    root_category = category_list.get('id')

    resp = instance.cms.category_handle(root_category, 'Test')
    assert resp.get('success'), resp.get('msg')
