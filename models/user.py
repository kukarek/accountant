from ..model import Model


class User(Model):

    @property
    def user_id(self): return self._user_id

    @property
    def username(self): return self._username

    def __init__(self, user_id, username):

        self._user_id = user_id
        self._username = username
