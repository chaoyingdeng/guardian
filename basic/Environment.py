from setting import env, tenant_id, account, password
from utils.decorator import Decorator


@Decorator.singleton
class Environment:
    def __init__(self):
        self._env = env
        self._tenant_id = tenant_id
        self._account = account
        self._password = password

    @property
    def env(self):
        return self._env

    @property
    def environment_dict(self):
        return {'env': self._env, 'tenant_id': self._tenant_id, 'account': self._account, 'password': self._password}

