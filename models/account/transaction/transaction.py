from ...model import Model
from enum import Enum
from dao import *


class Transactions_Categories(Enum):

    tips = "Чаевые"
    salary = "Зарплата"
    other = "Прочее"


class Transaction(Model):

    @property
    def datetime(self): return self._datetime

    @datetime.setter
    def datetime(self, datetime): self._datetime = datetime
    
    @property
    def amount(self): return self._amount
    
    @amount.setter
    def amount(self, amount): self._amount = amount

    @property
    def type(self): return self._type

    @type.setter
    def type(self, type): self._type = type

    @property
    def category(self): return self._category

    @category.setter
    def category(self, category): self._category = category

    def __init__(self, datetime = None, amount = None, category = None) -> None:
        
        self.datetime = datetime
        self.amount = amount
        self.category = category
    
    
