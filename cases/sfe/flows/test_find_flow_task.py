import allure
from utils.dates import today


@allure.title('日流向任务列表查询功能校验')
def start(instance):
    resp = instance.sfe_manage.flow_task_query(date_begin=today(), date_end=today())
    assert resp.json().get('data').get('pager').get('total')
