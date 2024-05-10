import allure
from utils.times import Times


@allure.title('拜访2.0流程验证')
def start(instance, user_info, ):
    temp_list = instance.crm.get_call_template_list(user_info, Times().today).json().get('data')
    institution_list = instance.crm.get_call_institution_list(user_info).json().get('data').get('records')
    if not temp_list or not institution_list:
        raise AssertionError

    instance.crm.get_customer_by_institution(institution_list[0].get('institutionId'), user_info)
