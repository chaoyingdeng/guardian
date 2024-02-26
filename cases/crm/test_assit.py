import pytest


@pytest.fixture
def handle_exception():
    try:
        yield
    except IndexError:
        pytest.fail("Caught IndexError in the tested function", pytrace=False)


@pytest.fixture
def start_function(handle_exception):
    def inner():
        raise ZeroDivisionError

    return inner


# test_example.py

def start(start_function):
    # 使用start_function fixture，它会抛出IndexError
    start_function()

# 如果你还有其他测试用例需要复用start_function fixture，
# 只需像上面那样在测试用例的参数列表中加上start_function即可。
