from business.saas_manage import SassManage
from business.sfe_manage import SfeManage
from business.crm_manage import CrmManage


class Instance:
    def __init__(self):
        self._sfe = SfeManage()
        self._saas = SassManage()
        self._crm = CrmManage()

    @property
    def sfe(self):
        return self._sfe

    @property
    def saas(self):
        return self._saas

    @property
    def crm(self):
        return self._crm
