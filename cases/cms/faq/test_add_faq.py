import allure
import setting
from pathlib import Path


@allure.title('FAQ新增流程校验')
def start(instance):
    category_list = instance.cms.get_category_list('FAQ')
    root_category = category_list.get('id')

    img_path = Path(__file__).parent.parent / 'data' / 'dog.jpg'
    file_path = instance.cms.file_upload(setting.tenant_id, img_path).get('relativeFileUrl')

    resp = instance.cms.add_faq(category_id=root_category, question_name='Test', file_path=file_path)
    assert resp, 'FAQ add Fail'
