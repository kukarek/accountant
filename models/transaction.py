from enum import Enum
from dao import *


class Transactions_Categories(Enum):

    tips = "Чаевые"
    salary = "Зарплата"
    other = "Прочее"


class Transaction():

    @property
    def datetime(self): return self._datetime
    
    @property
    def amount(self): return self._amount

    @property
    def type(self): return self._type

    @type.setter
    def type(self, t_type): self._type = t_type

    @property
    def category(self): return self._category

    def __init__(self, datetime = None, amount = None, category = None) -> None:
        
        self._datetime = datetime
        self._amount = amount
        self._category = category
    
    
