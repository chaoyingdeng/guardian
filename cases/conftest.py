import json, pytest, re, logging
from pathlib import Path
from business.instance import Instance
from datetime import datetime
from utils.paths import create_case_test_file_path
from utils.fakes import Fakers
from utils.excels import Excel
from functools import partial
from basic.exceptions import GuardianError


@pytest.fixture(name='instance', scope='session')
def setup_instance():
    instance = Instance()
    logging.info(f'instance_id = {id(instance)}')
    yield instance


@pytest.fixture(name='faker', scope='session')
def fake_manage():
    yield Fakers()


@pytest.fixture(name='case_file_name', scope='function')
def create_case_data_file_path(request):
    return re.findall(f'test[a-z0-9_]+', request.node.nodeid)[0]


@pytest.fixture(name='case_path_manage', scope='function')
def case_path_manage(case_file_name):
    return partial(create_case_test_file_path, case_file_name)


@pytest.fixture(name='excel', scope='function')
def excel_manage():
    yield Excel()


# -------------------------------------------------------------------------#
# pytest hooks                                                             #
# -------------------------------------------------------------------------#


def pytest_sessionstart(session):
    print('测试流程开始')


@pytest.hookimpl
def pytest_configure(config):
    config.addinivalue_line('markers', 'init: init case')
    config.addinivalue_line('markers', 'end: end case')
    config.addinivalue_line('markers', 'p0: p0 case')
    config.addinivalue_line('markers', 'p1: p1 case')


# @pytest.hookimpl
# def pytest_runtest_call(item):
#     """ 捕获用例中的已知异常,转换为断言异常
#     """ 不能这样使用，如果出现异常会导致重新调用测试套件
#     try:
#         item.runtest()
#     except GuardianError as e:
#         raise AssertionError('用例执行异常') from e


#
# @pytest.fixture(autouse=True)
# def guardian_error_handler(request):
#     print('123123')
#     def pytest_runtest_protocol(item, nextitem):
#         try:
#             yield
#         except GuardianError as e:
#             pytest.fail(f"GuardianError caught: {e}")
#     request.node.ihook.pytest_runtest_protocol = pytest_runtest_protocol


@pytest.hookimpl
def pytest_collection_modifyitems(session, config, items):
    """ 修改收集测试用例逻辑, 根据标记修改测试用例执行顺序 """
    init = []
    end = []
    remaining = []
    deselected = []

    def _check_case_name(case_item):
        return isinstance(case_item, pytest.Function) and case_item.name.startswith('start')

    def _check_case_marker(case_item, marker_name):
        return case_item.get_closest_marker(name=marker_name) is not None

    for item in items:
        if not _check_case_name(item):
            deselected.append(item)
        elif _check_case_marker(item, 'init'):
            init.append(item)
        elif _check_case_marker(item, 'end'):
            end.append(item)
        else:
            remaining.append(item)

    if init:
        remaining = init + remaining
    if end:
        # extend
        remaining += end
    if deselected:
        config.hook.pytest_deselected(items=deselected)

    items[:] = remaining


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_make_collect_report(collector):
#     # collector 类型是<_pytest.python.Module>或者package,因为有init方法
#     # 是一个收集用例的测试报告对象,每次收集到一个测试用例都会新建一个该对象
#     # report是一个CollectReport
#     out = yield
#     report = out.get_result()
#     if type(collector) is pytest.Module:
#         setattr(collector, 'report_collect', report)
#
#
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     """
#     每个测试用例的执行会调用三次该函数, 分别是执行时机 =setup,call,teardown
#     :param item:
#     :param call:
#     :return:
#     """
#     # 钩子函数前置执行完成后,会执行yield
#     # 保证其他钩子函数的执行,钩子函数必须这样写
#     out = yield
#     # 获取TestReport对象
#     res = out.get_result()
#     # 把report对象动态添加到了case属性中
#     setattr(item, "report_" + res.when, res)


@pytest.hookimpl
def pytest_terminal_summary(terminalreporter, config):
    # 筛选测试用例的辅助函数
    def filter_cases_by_prefix(case_items, prefix):
        return [case for case in case_items if prefix in case.nodeid]

    # 计算测试统计信息
    success_case_items = terminalreporter.stats.get('passed', [])
    fail_case_items = terminalreporter.stats.get('failed', [])
    case_num = len(success_case_items) + len(fail_case_items)

    crm_success_cases = filter_cases_by_prefix(success_case_items, 'cases/crm')
    crm_fail_cases = filter_cases_by_prefix(fail_case_items, 'cases/crm')
    sfe_success_cases = filter_cases_by_prefix(success_case_items, 'cases/sfe')
    sfe_fail_cases = filter_cases_by_prefix(fail_case_items, 'cases/sfe')

    # 构建测试汇总信息
    test_summary = {
        'total': case_num,
        'pass': len(success_case_items),
        'failed': len(fail_case_items),
        'sfe_total': len(sfe_success_cases) + len(sfe_fail_cases),
        'sfe_pass': len(sfe_success_cases),
        'sfe_failed': len(sfe_fail_cases),
        'crm_total': len(crm_success_cases) + len(crm_fail_cases),
        'crm_pass': len(crm_success_cases),
        'crm_failed': len(crm_fail_cases),
    }

    # 构建测试详细信息
    test_detail = {
        case.nodeid: 'fail' for case in fail_case_items
    }

    # 确保输出目录存在
    report_dir = Path(config.rootdir) / 'data' / 'report_related'

    report_file = report_dir / 'report.json'
    with report_file.open('w', encoding='utf-8') as f:
        json.dump(test_summary, f, ensure_ascii=False, indent=4)

    origin_report_file = report_dir / 'origin_report.json'
    with origin_report_file.open('w', encoding='utf-8') as f:
        json.dump(test_detail, f, ensure_ascii=False, indent=4)
