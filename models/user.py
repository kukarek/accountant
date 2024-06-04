from .transaction import Transaction
from dao import UserDAO


class User():

    @property
    def user_id(self): return self._user_id

    @property
    def username(self): return self._username

    def __init__(self, user_id, username):

        self._user_id = user_id
        self._username = username

        UserDAO.init(user_id, username)

    @property
    def name(self): return self._name

    @property
    def transactions(self):

        transactions = []

        for entry in UserDAO.transactions(self):

            #инициализция 
            transactions.append(Transaction(entry[0], entry[1], entry[2]))

        return transactions

    def update(self, transaction): UserDAO.update(self, transaction)

    def add_link(self, second_user): UserDAO.add_link(self, second_user)

    def remove_transaction(self, transaction_datetime): UserDAO.remove_transaction(transaction_datetime)


