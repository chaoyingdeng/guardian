import allure
from utils.times import Times


@allure.title('拜访2.0主流程验证')
def start(instance, user_info):
    # 获取拜访模板列表和机构列表
    temp_list = instance.crm.get_call_template_list(user_info, Times().today).json().get('data')
    institution_list = instance.crm.get_call_institution_list(user_info).json().get('data').get('records')

    assert temp_list, "No call templates found."
    assert institution_list, "No institutions found."

    template_id = temp_list[0].get('id')
    institution_id = institution_list[0].get('institutionId')

    customer_list_info = instance.crm.get_customer_by_institution(institution_id, user_info).json().get('data').get(
        'records')
    assert customer_list_info, "No customers found for the institution."

    called_customer_list_info = instance.crm.get_called_customer_list(institution_id=institution_id,
                                                                      call_date=Times().today).json().get('data')

    custom_list = {customer_info.get('id') for customer_info in customer_list_info}
    called_customer_list = {called_customer.get('id') for called_customer in called_customer_list_info}
    can_use_customer_list = (custom_list - called_customer_list)

    assert can_use_customer_list, 'NO Customers found for the institution.'

    customer_id = can_use_customer_list.pop()

    # 获取拜访模板的字段信息，并构建字段名到字典ID的映射
    dict_list = instance.crm.get_call_template_detail(template_id).json().get('data').get('displayFieldConfig').get(
        'basic').get('fields')
    assert dict_list, "No field configuration found for the call template."

    dicts = {dict_info.get('name'): dict_info.get('dictId') for dict_info in dict_list}
    call_type_id = dicts.get('CallType')
    call_purpose_id = dicts.get('CallPurpose')

    call_type = instance.saas.get_dict_detail_by_id(call_type_id).json().get('data')[0].get('dictionaryEntries')[0].get(
        'value')
    call_purpose = instance.saas.get_dict_detail_by_id(call_purpose_id).json().get('data')[0].get('dictionaryEntries')[
        0].get('value')

    resp = instance.crm.create_call_plan(
        customer_id,
        template_id=template_id,
        institution_id=institution_id,
        call_type=call_type,
        call_purpose=call_purpose,
        call_date=Times().today
    )

    assert resp, "Failed to create call plan"
