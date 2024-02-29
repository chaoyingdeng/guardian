import pytest


@pytest.hookimpl
def pytest_sessionstart(session):
    print(333)
