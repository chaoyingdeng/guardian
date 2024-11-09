from business.saas_manage import SassManage
from business.sfe_manage import SfeManage
from business.crm_manage import CrmManage
from business.cms_manage import CmsManage


class Instance:
    def __init__(self):
        self._sfe = SfeManage()
        self._saas = SassManage()
        self._crm = CrmManage()
        self._cms = CmsManage()

    @property
    def sfe(self):
        return self._sfe

    @property
    def saas(self):
        return self._saas

    @property
    def crm(self):
        return self._crm

    @property
    def cms(self):
        return self._cms
