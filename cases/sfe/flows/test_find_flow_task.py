import allure
from utils.times import Times
from utils.decorator import Decorator


@allure.title('日流向任务列表查询功能校验')
def start(instance):
    resp = instance.sfe.flow_task_query(date_begin=Times().today, date_end=Times().today)
    assert resp.json().get('data').get('pager').get('total')
