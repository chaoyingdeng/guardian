from utils.get_ini import get_ini


class Environment:

    def __init__(self):
        self._env = get_ini('env')

    @property
    def env(self):
        return self._env

    @classmethod
    def get(cls):
        env_dict = [get_ini('env'),
                    get_ini('tenant_id'),
                    get_ini('user_id'),
                    get_ini('user_name'),
                    get_ini('password')]
        return env_dict

