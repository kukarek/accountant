from dao import AccountDAO
from .transaction import Transaction

class Account():
    
    @property
    def name(self): return self._name

    @property
    def transactions(self):

        transactions = []
        a = AccountDAO.transactions(self)
        for entry in AccountDAO.transactions(self):

            #создание обьектов из данных бд
            transactions.append(Transaction(entry[0], entry[1], entry[2]))

        return transactions


    #создание таблицы для нового пользователя
    def __init__(self, user_id):  

        self._name = f"user_{user_id}"

        AccountDAO.create_table(self)

    def update(self, transaction): AccountDAO.update(self, transaction)

    def add_link(self): pass

    def remove_transaction(self, transaction_datetime): AccountDAO.remove_transaction(self, transaction_datetime)


      