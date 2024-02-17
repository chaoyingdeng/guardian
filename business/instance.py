import business.sfe_manage


class Instance:
    def __init__(self):
        self._sfe_manage = business.sfe_manage.connect()

    @property
    def sfe_manage(self):
        return self._sfe_manage
