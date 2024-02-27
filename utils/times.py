from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.decorator import Decorator


@Decorator.singleton
class Times:
    """ 添加单例模式只能避免跨天问题, 无法解决跨月"""

    def __init__(self):
        self._now = datetime.now()

    @property
    def year(self):
        return self._now.strftime(f'%Y')

    @property
    def month(self):
        return self._now.strftime(f"%m")

    @property
    def pre_month(self):
        return (self._now - relativedelta(months=1)).strftime("%m")

    @property
    def today(self):
        return self._now.strftime(f'%Y-%m-%d')


if __name__ == '__main__':
    print(Times().today)
