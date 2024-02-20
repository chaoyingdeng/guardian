from business.saas_manage import SassManage
from business.sfe_manage import SfeManage


class Instance:
    def __init__(self):
        self._sfe = SfeManage()
        self._saas = SassManage()

    @property
    def sfe(self):
        return self._sfe

    @property
    def saas(self):
        return self._saas
