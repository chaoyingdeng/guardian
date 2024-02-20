from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.decorator import Decorator


@Decorator.singleton
class Times:
    @property
    def year(self):
        return datetime.now().strftime(f'%Y')

    @property
    def month(self):
        return datetime.now().strftime(f"%m")

    @property
    def pre_month(self):
        return (datetime.now() - relativedelta(month=1)).strftime(f"%m")

    @property
    def today(self):
        return datetime.now().strftime(f'%Y-%m-%d')
