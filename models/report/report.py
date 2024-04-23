from ..model import Model 
from ..account import Account


class Report(Model):

    @property
    def accounts(self): return self._accounts 

    def __init__(self) -> None:
        pass

    def per_month(self):
        pass

    def all_time(self):
        pass

    def for_the_period(self):
        pass