from basic.exceptions import GuardianError
from basic.exceptions import ExcelNotLoadError
from utils.decorator import Decorator


@Decorator.handle_guardian_error
def test_one():
    raise ExcelNotLoadError("Failed to load Excel file")
