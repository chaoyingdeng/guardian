import pytest


@pytest.hookimpl
def pytest_sessionstart(session):
    from pathlib import Path
    print(333)
