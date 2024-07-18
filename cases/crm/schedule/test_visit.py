import pytest


# 参数化示例函数
@pytest.mark.parametrize("input", [1])
def start(input):
    print(input)
    assert input == 1
